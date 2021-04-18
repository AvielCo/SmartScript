import './Home.css';
import { NavBar, ResultTextView } from '../../components';
import React, { useState, useEffect } from 'react';
import pic from '../../assets/landing-bg.jpg';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import { getAccessToken } from '../../helpers';
import { Upload } from 'antd';
import Card from '../../components/Card/ProfileCard';
import Button from '../../components/Buttons/InputButton';

import cursive from '../../assets/cursive_trans.png';

import Emilia from '../../assets/emilia.jpg';
import Noah from '../../assets/noah.png';
import Aviel from '../../assets/aviel.png';

function LandingSection() {
  return (
    <section className='landing'>
      <div>
        <p dir='rtl'>
          <h2>SmartScript</h2> was developed to solve the problem in categorizing hebrew ancient scripts. This website will identify the origin and the shape of the script given to it by scanning the
          image given to it by the user. Additionally, the system will allow the user to save previous uploads for easy tracking.
        </p>
      </div>
    </section>
  );
}

function ScanSection({ isLoggedIn }) {
  const [imageUri, setImageUri] = useState();
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
        console.log(info.file.originFileObj);
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

  return (
    <section className='scan'>
      <div className='scan-container'>
        {isLoggedIn ? (
          <form className='scan-btn-holder' onSubmit={handleImageChange}>
            <h3>Upload and Predict</h3>
            <Upload
              action='http://localhost:8008/api/images/upload'
              headers={{ Authorization: 'Bearer ' + getAccessToken() }}
              onChange={handleImageChange}
              accept='image/*'
              maxCount={1}
              showUploadList={false}
            >
              <Button className='scan-btn' component='span' type='submit' name={'Upload'} disabled={isLoading}></Button>
            </Upload>
            <Button className='scan-btn' onClick={handlePredict} name={'Predict'} disabled={isLoading}></Button>

            <div className='scan-btn'></div>

            <ResultTextView result={result} />
          </form>
        ) : (
          <div>Login so you can scan</div>
        )}
        {imageUri && (
          <div className='scan-img-holder'>
            <img alt={pic} src={imageUri}></img>
          </div>
        )}
      </div>
    </section>
  );
}

function AboutSection() {
  return (
    <section className='about'>
      <h3>About the project</h3>

      <div className='about-content'>
        <div className='about-text-holder'>
          <p>
            By uploading an image and pressing the scan button the system will scan the image and return a predicted value for that given image. The system does it by spliting the image into 2 single
            paged images if the image contains 2 pages followed by dividing the image into small resolutions patches.
          </p>
          <p>
            Then it applies binarization on these patches so it can filter unnecessary areas from the original image. These areas might contain noisy data (salt and pepper) or just plain colored areas
            without text based on the ratio between the black and the white pixels.
          </p>
          <p>After the filtering is done the corresponding orignal patches are saved in grayscale and used to predict the origin and the shape of the script.</p>
        </div>
        <div className='image-rotate-holder'>
          <img className='rotating-image' alt='something' src={cursive}></img>
        </div>
      </div>
    </section>
  );
}

function WWASection() {
  return (
    <section className='wwa'>
      <h3>Who we are</h3>
      <div className='cards-holder'>
        <Card name={'Noah Solomon'} image={Noah} />
        <Card name={'Emilia Zorin'} image={Emilia} />
        <Card name={'Aviel Cohen'} image={Aviel} />
      </div>
    </section>
  );
}

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const history = useHistory();

  useEffect(() => {
    if (isLoggedIn) return;
    const cfg = {
      headers: {
        Authorization: 'Bearer ' + getAccessToken(),
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
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace('/404');
            return;
          }
        } else {
          alert('Internal Server Error');
        }
      });
  }, [isLoggedIn]);

  return (
    <div className='home'>
      <NavBar isLoggedIn={isLoggedIn} />
      <LandingSection />
      <ScanSection isLoggedIn={isLoggedIn} />
      <AboutSection />
      <WWASection />
    </div>
  );
}
export default Home;
