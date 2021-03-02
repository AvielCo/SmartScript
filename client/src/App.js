import "./App.css";
import InputButton from "./components/Buttons/InputButton";

function App() {
  return (
    <div className="Scan">
      <InputButton name="Upload Image"></InputButton>
      <InputButton name="Scan Selected Image"></InputButton>
    </div>
  );
}
export default App;