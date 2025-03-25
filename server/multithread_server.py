import random
from flask import Flask, request, jsonify, send_from_directory
import concurrent.futures
import uuid
import time
from flask_cors import CORS
import psutil
from functools import wraps
from interpreter.src.interpreter_handler import Interpreter
from interpreter.src.journal.journal import JournalSettings
from interpreter.src.journal.journal_events import ErrorEvent, PrintEvent

app = Flask(__name__, static_folder="../client/dep_web/dist", static_url_path="/")
CORS(app)  # Allow requests from React frontend

# If the task takes less than this time, we just return it on submit (to prevent extra requests)
MIN_TASK_WAIT_SECONDS = 0.1
MAX_WORKERS = 4
MAX_VRAM_USAGE_PERCENT = 99
DEFAULT_TIMEOUT_SECONDS = 5

whitelist = [
    PrintEvent,
    ErrorEvent,
]
RUN_JOURNAL_SETTINGS = JournalSettings(whitelist)
DEBUG_JOURNAL_SETTINGS = JournalSettings()

# Configure thread pool
executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

task_results = {}

def timeout_handler(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=seconds)
            except concurrent.futures.TimeoutError:
                return {"status": "timeout", "message": f"Task exceeded {seconds} seconds"}
        return wrapper
    return decorator

@timeout_handler(DEFAULT_TIMEOUT_SECONDS)
def execute_code(request_data):
    try:
        interpreter = Interpreter(RUN_JOURNAL_SETTINGS, True)
        journal = interpreter.feedBlock(request_data)
        return {"status": "completed", "result": journal.serialize()}
    except Exception as e:
        print(f'[Server Error] {e}')
        return {"status": "error", "message": "Unhandled exception"}

@timeout_handler(DEFAULT_TIMEOUT_SECONDS)
def debug_code(request_data):
    try:
        interpreter = Interpreter(DEBUG_JOURNAL_SETTINGS, True)
        journal = interpreter.feedBlock(request_data)
        return {"status": "completed", "result": journal.serialize()}
    except Exception as e:
        print(f'[Server Error] {e}')
        return {"status": "error", "message": "Unhandled exception"}

@app.route('/api/submit', methods=['POST'])
def submit_task():
    memory_usage = psutil.virtual_memory().percent

    if memory_usage > MAX_VRAM_USAGE_PERCENT:
        return jsonify({"status": "error", "message": "Server too busy, try again later"}), 503
    
    if len(task_results) >= MAX_WORKERS:
        return jsonify({"status": "error", "message": "Server too busy, try again later"}), 503
    
    request_data = request.json.get('data')
    is_debug = request.json.get('is_debug')
    code_handler_func = debug_code if is_debug else execute_code
    
    task_id = str(uuid.uuid4())
    
    # Submit and store task
    future = executor.submit(code_handler_func, request_data)
    task_results[task_id] = {
        "future": future,
        "submitted_at": time.time()
    }
    
    return jsonify({"status": "accepted", "task_id": task_id})

@app.route('/api/result/<task_id>', methods=['GET'])
def get_result(task_id):
    if task_id not in task_results:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    
    task = task_results[task_id]
    future = task["future"]
    
    if not future.done():
        elapsed = time.time() - task["submitted_at"]
        return jsonify({"status": "pending", "elapsed_seconds": elapsed})
    
    try:
        result = future.result(timeout=0)
        del task_results[task_id]
        return jsonify(result)
    except concurrent.futures.TimeoutError:
        return jsonify({"status": "timeout", "message": "Task timed out"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/status', methods=['GET'])
def server_status():
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    
    return jsonify({
        "active_tasks": len(task_results),
        "memory_usage": memory_usage,
        "cpu_usage": cpu_usage,
        "max_workers": MAX_WORKERS
    })

@app.route('/')
def home():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(debug=True)