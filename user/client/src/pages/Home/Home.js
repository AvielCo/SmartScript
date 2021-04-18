import React, { useState, useEffect } from 'react';
import { NavBar, ResultTextView } from '../../components';
import pic from '../../assets/landing-bg.jpg';
import { ToastContainer, toast } from 'react-toastify';
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

import 'react-toastify/dist/ReactToastify.css';
import './Home.css';

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
    if (!imageUri) {
      toast.error('Upload an image before predict.');
      return;
    }
    if (isLoading) {
      toast.info('Please wait, another predict process is running.');
      return;
    }
    toast.info('Predicting image, please wait.');
    setIsLoading(true);

    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };

    axios
      .post(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/images/scan`, null, cfg)
      .then((res) => {
        if (res.status === 200) {
          setResult(res.data);
          setIsLoading(false);
          toast.success('Predicting image done, see the result in your profile page.');
        }
      })
      .catch((err) => {
        if (err) {
          toast.error('An error has been encountered while trying to predict.');
          setIsLoading(false);
        }
      });
  };

  return (
    <section className='scan'>
      <div className='scan-container'>
        {isLoggedIn ? (
          <form className='scan-btn-holder' onSubmit={handleImageChange}>
            <h3>Upload and Predict</h3>
            <Upload
              action={`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/images/upload`}
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
          <h3>
            Please login to gain access to the "Scan" feature. <br /> Consider registering if you don't have an account.
          </h3>
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
      <p>
        We are 4th year Software Engineering students at SCE Sami Shamoon. We decided to join Dr. Irina Rabaev and with her guidance tackle this challenge. During summer time and the first semester we
        researched and experimented with different models and architectures and strive for high accuracies with the limitations and the challenges presented to us during the Covid outbreak in 2020.
      </p>
      <p>
        In the second semester we shifted towards developing the website that will allow paleographers to easily classify hebrew scripts with ease. We focused on developing strong functionality from
        front to back. Combining RESTapi to handle requests and JWT we developed a secure login and registration. Additionally, we made sure that our website will be functional and resonsive on
        different devices and resolutions
      </p>
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
      .get(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/user`, cfg)
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
          toast.info('Please log in to upload and predict an image.');
        }
      });
  }, [isLoggedIn]);

  return (
    <>
      <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className="home">
        <NavBar isLoggedIn={isLoggedIn} />
        <LandingSection />
        <ScanSection isLoggedIn={isLoggedIn} />
        <AboutSection />
        <WWASection />
      </div>
    </>
  );
}
export default Home;
