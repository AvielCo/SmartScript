
import './Home.css';
import NavBar from '../../components/NavBar/NavBar';
import TextView from '../../components/TextView/TextView';
import InputButton from '../../components/Buttons/InputButton';
import React, { useState } from 'react';
import pic from '../../assets/landing-bg.jpg';
import axios from 'axios';

function Home() {
  const [imageUrl, setImageUrl] = useState();

  const handleImageChange = async (event) => {
    const fd = new FormData();
    fd.append('file', event.target.files[0]);

    axios
      .post('http://localhost:8008/api/images/upload', fd, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((res) => console.log(res));

    setImageUrl(URL.createObjectURL(event.target.files[0]));
  };

  const handleScanSubmit = (event) => {
    console.log(event);
  };

  return (
    <div>
      <NavBar />
      <section className='landing'>
        <div></div>
        <p>
          Elit eiusmod elit ut id esse velit veniam ut consectetur esse occaecat quis sunt. Duis cupidatat qui sint ipsum amet exercitation enim et ipsum proident nostrud proident dolor. Incididunt
          officia voluptate aute commodo sit anim non et cupidatat cillum elit veniam. Irure anim aliquip enim officia anim voluptate minim mollit Lorem cillum. Consectetur est in magna labore nulla
          adipisicing ex aute Lorem. Cupidatat ipsum sit ut consequat minim aliquip consequat.
        </p>
      </section>

      <section className="scan">
        <div className="scan-container">
          <form className="btn-holder" onSubmit={handleScanSubmit}>
            <h3>Scan Image</h3>
            <input style={{ display: 'none' }} accept="image/*" type="file" id="upload-file-btn" onChange={handleImageChange} />
            <label htmlFor="upload-file-btn">
              <InputButton name="Upload Image" component="span" type="submit" />
            </label>
            <InputButton name="Scan Selected Files" />
            <TextView />
          </form>
          <div className="img-holder">
            <img alt={pic} src={imageUrl}></img>

          </div>
        </div>
      </section>
      <section className='about'></section>
      <section className='wwa'></section>
    </div>
  );
}
export default Home;
