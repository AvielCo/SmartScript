import './Home.css';
import NavBar from '../../components/NavBar/NavBar';
import React, { useState } from 'react';
import pic from '../../assets/landing-bg.jpg';
import axios from 'axios';
import { getAccessToken } from '../helpers';
import { Button, Upload, message } from 'antd';

function LandingSection() {
  return (
    <section className="landing">
      <div></div>
      <p>
        Elit eiusmod elit ut id esse velit veniam ut consectetur esse occaecat quis sunt. Duis cupidatat qui sint ipsum amet exercitation enim et ipsum proident nostrud proident dolor. Incididunt
        officia voluptate aute commodo sit anim non et cupidatat cillum elit veniam. Irure anim aliquip enim officia anim voluptate minim mollit Lorem cillum. Consectetur est in magna labore nulla
        adipisicing ex aute Lorem. Cupidatat ipsum sit ut consequat minim aliquip consequat.
      </p>
    </section>
  );
}

function ScanSection() {
  const [imageUri, setImageUri] = useState();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState({
    success: false,
    origin: '',
    shape: '',
    probability: '',
  });

  const handleImageChange = async (info) => {
    switch (info.file.status) {
      case 'uploading':
        setIsLoading(true);
        break;
      case 'done':
        setIsLoading(false);
        setImageUri(URL.createObjectURL(info.file.originFileObj));
        break;
      case 'error':
        setIsLoading(false);
        break;
      default:
        break;
    }
  };

  const handlePredict = () => {
    if (!imageUri || isLoading) return;
    setIsLoading(true);

    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };

    axios
      .post('http://localhost:8008/api/images/scan', null, cfg)
      .then((res) => {
        if (res.status === 200) {
          setResult(res.data);
          return;
        }
        console.log(res.data);
      })
      .then(() => {
        setIsLoading(false);
      })
      .catch((err) => {
        setIsLoading(false);
      });
  };

  useEffect(() => {
    if (isLoggedIn) return;

    //get token from sessionStorage, if undefined => get token from localStorage.
    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };

    axios
      .get('http://localhost:8008/api/auth/user', cfg)
      .then((res) => {
        if (res.status === 200) {
          setIsLoggedIn(true);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [isLoggedIn]);

  return (
    <section className="scan">
      <div className="scan-container">
        {isLoggedIn ? (
          <form className="scan-btn-holder" onSubmit={handleImageChange}>
            <h3>Scan Image</h3>
            <Upload
              action="http://localhost:8008/api/images/upload"
              headers={{ Authorization: 'Bearer ' + getAccessToken() }}
              onChange={handleImageChange}
              accept="image/*"
              maxCount={1}
              showUploadList={false}>
              <Button className="scan-btn" component="span" type="submit" loading={isLoading}>
                Upload an image
              </Button>
            </Upload>
            <Button className="scan-btn" onClick={handlePredict} loading={isLoading}>
              Predict selected image
            </Button>
            <ResultTextView result={result} />
          </form>
        ) : (
          <div>Login so you can scan</div>
        )}
        {imageUri && (
          <div className="scan-img-holder">
            <img alt={pic} src={imageUri}></img>
          </div>
        )}
      </div>
    </section>
  );
}

function AboutSection() {
  return <section className="about"></section>;
}

function WWASection() {
  return <section className="wwa"></section>;
}

function Home() {
  return (
    <div className="home">
      <NavBar />
      <LandingSection />
      <ScanSection />
      <AboutSection />
      <WWASection />
    </div>
  );
}
export default Home;
