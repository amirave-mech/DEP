import React from 'react';
import './App.css';
import { CodeModule } from './CodeModule';
import { OutputModule } from './OutputModule';

declare var __API_DOMAIN__: string;

var domain: string = __API_DOMAIN__

function App() {
  const [codeText, setCodeText] = React.useState('print("hello world!")');
  const [output, setOutput] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [serverMessage, setServerMessage] = React.useState('');

  const onCodeTextChange = React.useCallback((val: React.SetStateAction<string>) => {
    setCodeText(val);
  }, []);

  const runCode = async (isDebug: boolean) => {
    if (!codeText) return;

    setIsLoading(true);
    setError('');
    setOutput('');
    setServerMessage('');

    const response = await fetchData(codeText, isDebug);
    if (response.status == "error") {
      setError('Error executing code');
      setServerMessage(response.message || 'Unknown error occurred');
    } else if (response.status == "timeout") {
      setError('Timeout occurred');
      setServerMessage(response.message || 'Request timed out');
    } else {
      setOutput(JSON.stringify(response.result));
    }

    setIsLoading(false);
  };

  return (
    <>
      <Header></Header>
      <div className="main-content">
        <div className="left-side">
          <CodeModule
            value={codeText}
            onChange={onCodeTextChange}
          />
        </div>

        <div className="right-side">
          <OutputModule
            runCode={() => runCode(false)}
            runDebug={() => runCode(true)}
            outputText={output}
            isLoading={isLoading}
            error={error}
            serverMessage={serverMessage}
          />
        </div>
      </div>
    </>
  )
}

function Header() {
  return (
    <div className='header'>
      <h1 className='title'>Pcode</h1>
    </div>
  )
}

// Submit a task to the server
async function submitTask(taskData: string, isDebug: boolean) {
  try {
    console.log(domain);
    const response = await fetch(`${domain}/api/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ data: taskData, is_debug: isDebug })
    });

    const result = await response.json();

    if (response.ok) {
      console.log(`Task submitted successfully with ID: ${result.task_id}`);
      return result.task_id;
    } else {
      console.error(`Error submitting task: ${result.message}`);
      return null;
    }
  } catch (error) {
    console.error('Failed to submit task:', error);
    return null;
  }
}

// Check the status of a submitted task
async function checkTaskStatus(taskId: string): Promise<any> {
  try {
    const response = await fetch(`${domain}/api/result/${taskId}`);
    const result = await response.json();

    return result;
  } catch (error) {
    console.error(`Failed to check task status for ${taskId}:`, error);
    return { status: 'error', message: 'Failed to connect to server' };
  }
}

// Poll for task results until completion
async function pollForResults(taskId: string, pollingInterval = 1000): Promise<any> {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const result = await checkTaskStatus(taskId);

        // If task is still pending, continue polling
        if (result.status === 'pending') {
          console.log(`Task ${taskId} still processing... (${result.elapsed_seconds?.toFixed(1) || '?'}s elapsed)`);
          setTimeout(poll, pollingInterval);
        }
        // If task is complete or has an error, resolve with the result
        else {
          console.log(`Task ${taskId} finished with status: ${result.status}`);
          resolve(result);
        }
      } catch (error) {
        reject(error);
      }
    };

    poll();
  });
}

// {"status": "completed", "result": journal}
// {"status":"timeout/error", "message": "bla bla"}
async function fetchData(text: string, isDebug: boolean): Promise<any> {
  try {
    // Submit the task
    const taskId = await submitTask(text, isDebug);

    if (!taskId) {
      return { status: "error", message: 'Failed to submit task' };
    }

    // Poll for results until completion
    const result = await pollForResults(taskId, 1000);

    return result;
  } catch (error) {
    console.error('Error processing task: ', error);
    return { status: "error", message: 'Request failed, please try again.' };
  }
}

export default App;