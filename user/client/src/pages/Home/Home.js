import React, { useState } from 'react';
import { NavBar, ResultTextView } from '../../components';
import pic from '../../assets/landing-bg.jpg';
import { ToastContainer, toast } from 'react-toastify';
import axios from 'axios';

import { getAccessToken } from '../../helpers';
import { Upload } from 'antd';
import Button from '../../components/Buttons/InputButton';
import { HashLink as HashLink } from 'react-router-hash-link';

import 'react-toastify/dist/ReactToastify.css';
import './Home.css';

function LandingSection() {
  return (
    <section className='landing'>
      <div className='landing-div'>
        <p>
          <bold>SmartScript</bold> was developed to solve the problem in categorizing hebrew ancient scripts. This website will identify the origin and the shape of the script given to it by scanning
          the image given to it by the user. Additionally, the system will allow the user to save previous uploads for easy tracking.
        </p>
        <HashLink to='home#scan' smooth>
          <Button className='move-to-scan' name={'Proceed to predict an image'}></Button>
        </HashLink>
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
      .post(`${process.env.REACT_APP_API_ADDRESS}/api/images/scan`, null, cfg)
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
    <section className='scan' id='scan'>
      <div className='scan-container'>
        <form className='scan-btn-holder' onSubmit={handleImageChange}>
          <h3>Upload and Predict</h3>
          <p>Upload an image and click on predict to see results!</p>
          <Upload
            action={`${process.env.REACT_APP_API_ADDRESS}/api/images/upload`}
            headers={{ Authorization: 'Bearer ' + getAccessToken() }}
            onChange={handleImageChange}
            accept='image/*'
            maxCount={1}
            showUploadList={false}
          >
            <Button className='scan-btn' component='span' type='submit' name={'Upload'} disabled={isLoading} />
          </Upload>
          <Button className='scan-btn' onClick={handlePredict} name={'Predict'} disabled={isLoading}></Button>
          <div className='scan-btn'></div>
          <ResultTextView result={result} />
        </form>

        {imageUri && (
          <div className='scan-img-holder'>
            <img alt={pic} src={imageUri}></img>
          </div>
        )}
      </div>
    </section>
  );
}

function Home({ isLoggedIn, setIsLoggedIn }) {
  return (
    <>
      <ToastContainer position='top-left' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className='home' id='home'>
        <NavBar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
        <LandingSection />
        <ScanSection isLoggedIn={isLoggedIn} />
      </div>
    </>
  );
}
export default Home;
