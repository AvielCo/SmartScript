import './App.css';
import { Grid, Typography } from '@material-ui/core';
import NavBar from './components/NavBar/NavBar';
import landingImage from './assets/coolimage.jpg';

function App() {
  return (
    <div>
      <NavBar />
      <section className="landing">
        <div></div>
        <p>
          Elit eiusmod elit ut id esse velit veniam ut consectetur esse occaecat quis sunt. Duis cupidatat qui sint ipsum amet exercitation enim et ipsum proident nostrud proident dolor. Incididunt
          officia voluptate aute commodo sit anim non et cupidatat cillum elit veniam. Irure anim aliquip enim officia anim voluptate minim mollit Lorem cillum. Consectetur est in magna labore nulla
          adipisicing ex aute Lorem. Cupidatat ipsum sit ut consequat minim aliquip consequat.
        </p>
      </section>
      <section className="scan"></section>
      <section className="about"></section>
      <section className="wwa"></section>
    </div>
  );
}
export default App;
