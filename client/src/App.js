import './App.css';
import NavBar from './components/NavBar/NavBar';
import TextView from './components/TextView/TextView';
import InputButton from './components/Buttons/InputButton';
import React , {useState} from 'react';
import pic from './assets/landing-bg.jpg';



function App() {
  return (
    <div>
      <NavBar />
      <section className="landing">
        <div></div>
        <p>
          Elit eiusmod elit ut id esse velit veniam ut consectetur esse occaecat
          quis sunt. Duis cupidatat qui sint ipsum amet exercitation enim et
          ipsum proident nostrud proident dolor. Incididunt officia voluptate
          aute commodo sit anim non et cupidatat cillum elit veniam. Irure anim
          aliquip enim officia anim voluptate minim mollit Lorem cillum.
          Consectetur est in magna labore nulla adipisicing ex aute Lorem.
          Cupidatat ipsum sit ut consequat minim aliquip consequat.
        </p>
      </section>
      <section className="scan">
        <div className="scan-container">
          <div className="btn-holder">
            <h3>Scan Image</h3>
            <InputButton name="Upload Image" />
            <InputButton name="Scan Selected Files" />
            <TextView/>
          </div>
          <div className="img-holder">
            <img alt="something" src={pic}></img>
          </div>
        </div>
      </section>
      <section className="about"></section>
      <section className="wwa"></section>
    </div>
  );
}
export default App;
