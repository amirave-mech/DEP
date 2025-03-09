import './App.css'

function App() {
  const sendCode = () => {
    let textArea: HTMLInputElement | null = document.getElementById('code') as HTMLInputElement;
    let serverResponse: HTMLElement | null = document.getElementById('serverResponse');
    if (textArea && serverResponse) {
      fetchData(textArea.value).then(data => serverResponse.innerHTML = (data.received).replace(/\n/g, '<br>') || data.error);
    }
  }

  return (
    <>
      <Header></Header>
      <div className="main-content">
        <div className="left-side">
          <h1>Enter your text here</h1>
          <textarea id='code'></textarea><br />
        </div>

        <div className="right-side">
          <button onClick={sendCode}>Send Text</button><br />
          <p id='serverResponse' />
        </div>
      </div>
    </>
  )
}

function Header() {
  return (
    <div className='header'>
      <h1 className='title'>Dipsy</h1>
    </div>
  )
}

async function fetchData(text: string) {
  try {
    const options: RequestInit = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(text) };
    return fetch('http://localhost:5000/', options).then(response => response.json());
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
}

export default App
