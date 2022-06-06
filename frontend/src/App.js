import logo from './logo.svg';
import './App.css';
import { testEP } from "./api/sales"

function App() {

  const Test = async () => {
    try {
      const data = new FormData()
      data.append('bool', true)
      const response = await testEP(data)
    } catch (error) {
      console.log(error.response)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={Test}>LOL</button>
      </header>
    </div>
  );
}

export default App;
