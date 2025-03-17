// JavaScript client for interacting with the thread pool server

// Submit a task to the server
async function submitTask(taskData) {
    try {
      const response = await fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: taskData })
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
  async function checkTaskStatus(taskId) {
    try {
      const response = await fetch(`http://localhost:5000/result/${taskId}`);
      const result = await response.json();
      
      return result;
    } catch (error) {
      console.error(`Failed to check task status for ${taskId}:`, error);
      return { status: 'error', message: 'Failed to connect to server' };
    }
  }
  
  // Poll for task results until completion
  async function pollForResults(taskId, pollingInterval = 1000) {
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const result = await checkTaskStatus(taskId);
          
          // If task is still pending, continue polling
          if (result.status === 'pending') {
            console.log(`Task ${taskId} still processing... (${result.elapsed_seconds.toFixed(1)}s elapsed)`);
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
      
      // Start polling
      poll();
    });
  }
  
  // Check server status
  async function checkServerStatus() {
    try {
      const response = await fetch('http://localhost:5000/status');
      const status = await response.json();
      
      console.log('Server status:', status);
      return status;
    } catch (error) {
      console.error('Failed to check server status:', error);
      return null;
    }
  }
  
  // Example usage
  async function processTask() {
    // Display UI elements
    document.getElementById('status').textContent = 'Submitting task...';
    
    // Check server load before submitting
    // const serverStatus = await checkServerStatus();
    // if (serverStatus && serverStatus.memory_usage > 80) {
    //   document.getElementById('status').textContent = 'Server is busy, try again later';
    //   return;
    // }
    
    // Get task data from form
    const taskData = document.getElementById('taskInput').value;
    
    // Submit the task
    const taskId = await submitTask(taskData);
    
    if (!taskId) {
      document.getElementById('status').textContent = 'Failed to submit task';
      return;
    }
    
    document.getElementById('status').textContent = `Task submitted (ID: ${taskId}). Waiting for results...`;
    
    // Poll for results
    try {
      const result = await pollForResults(taskId, 2000); // Check every 2 seconds
      
      if (result.status === 'completed') {
        document.getElementById('status').textContent = 'Task completed!';
        document.getElementById('result').textContent = JSON.stringify(result, null, 2);
      } else {
        document.getElementById('status').textContent = `Task failed: ${result.message}`;
      }
    } catch (error) {
      document.getElementById('status').textContent = `Error: ${error.message}`;
    }
  }