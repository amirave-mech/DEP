import './App.css'

function App() {
  const sendCode = () => {
    let textArea: HTMLInputElement | null = document.getElementById('code') as HTMLInputElement;
    let serverResponse: HTMLElement | null = document.getElementById('serverResponse');
    if (textArea && serverResponse) {
      fetchData(textArea.value).then(data => serverResponse.textContent = (data.message + data.received) || data.error);
    }
  }

  return (
    <>
      <h1>Enter your text here</h1>
      <textarea id='code'></textarea><br/>
      <button onClick={sendCode}>Send Text</button><br/>
      <p id='serverResponse'/>
    </>
  )
}

async function fetchData(text: string) {
  try {
    const options: RequestInit = {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(text)};
    return fetch('http://locaclhost:5000/', options).then(response => response.json());
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
}

export default App
