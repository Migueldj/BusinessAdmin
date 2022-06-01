import logo from './logo.svg';
import './App.css';
import { createSale } from "./api/sales"

function App() {

  const CreateSale = async () => {
    try {
      // const obj = {
      //   products: [{"name":"lol"}, {"name":"xd"}],
      //   name: "Miguel",
      //   age: 22
      // }
      const data = new FormData()
      data.append('products', JSON.stringify([{"name":"lol", "quantity":2}, {"name":"xd", "quantity":5}]))
      const response = await createSale(data)
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
        <button onClick={CreateSale}>LOL</button>
      </header>
    </div>
  );
}

export default App;
