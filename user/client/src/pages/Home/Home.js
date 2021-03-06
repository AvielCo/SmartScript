import React, { useState } from "react";
import { NavBar, ResultTextView } from "../../components";
import pic from "../../assets/landing-bg.jpg";
import { ToastContainer, toast } from "react-toastify";
import axios from "axios";
import { getAccessToken } from "../../helpers";
import { Upload } from "antd";
import Button from "../../components/Buttons/InputButton";
import { HashLink as HashLink } from "react-router-hash-link";

import "react-toastify/dist/ReactToastify.css";
import "./Home.css";

function LandingSection() {
  return (
    <section className="landing">
      <div className="landing-div">
        <p>
          <bold>SmartScript</bold>
          <br />
          This webpage was developed to recognize types and sub-types of medieval Hebrew scripts.
          <br />
          Please upload your manuscript page.
        </p>
        <HashLink to="home#scan" smooth>
          <Button className="move-to-scan" name={"Proceed to predict an image"}></Button>
        </HashLink>
      </div>
    </section>
  );
}

function ScanSection({ isLoggedIn }) {
  const [imageUri, setImageUri] = useState();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState();
  const [savedToHistory, setSavedToHistory] = useState({
    saved: true,
    reason: "",
  });

  const [result, setResult] = useState({
    success: false,
    origin: "",
    shape: "",
    probability: "",
  });

  const handleImageChange = async (event) => {
    event.preventDefault();
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
      setImageUri(URL.createObjectURL(event.target.files[0]));
    }
  };

  const handlePredict = (event) => {
    event.preventDefault();
    if (!imageUri && !selectedImage) {
      toast.error("Upload an image before predict.");
      return;
    }
    if (isLoading) {
      toast.info("Please wait, another predict process is running.");
      return;
    }
    toast.info("Predicting image, please wait.");
    setIsLoading(true);

    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
        "content-type": "multipart/form-data",
      },
    };

    const fd = new FormData();
    fd.append("file", selectedImage, selectedImage.name);

    axios
      .post(`${process.env.REACT_APP_API_ADDRESS}/api/images/predict`, fd, getAccessToken() ? cfg : { headers: { "content-type": "multipart/form-data" } })
      .then((res) => {
        if (res.status === 200) {
          const { savedToHistory: saved, reason } = res.data;
          if (!saved) {
            setSavedToHistory({ saved, reason });
          }
          toast.success("Predicting image done.");
          setResult(res.data);
          setIsLoading(false);
        }
      })
      .catch((err) => {
        if (err) {
          toast.error("An error has been encountered while trying to predict.");
          setIsLoading(false);
        }
      });
  };

  return (
    <section className="scan" id="scan">
      <div className="scan-container">
        <form className="scan-btn-holder" onSubmit={handlePredict}>
          <h3>Upload and Predict</h3>
          {!getAccessToken() && (
            <p>
              Please consider signing up to save previous uploads for future use. <br /> This will take less than a minute.
            </p>
          )}
          <input accept="image/*" onChange={handleImageChange} id="upload-button" type="file" style={{ display: "none" }} />
          <label htmlFor="upload-button">
            <Button className="scan-btn" component="span" name={"Upload"} disabled={isLoading} />
          </label>
          <Button className="scan-btn" type="submit" name={"Predict"} disabled={isLoading}></Button>

          <ResultTextView result={result} savedToHistory={savedToHistory} />
        </form>

        {imageUri && (
          <div className="scan-img-holder">
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
      <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className="home" id="home">
        <NavBar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
        <LandingSection />
        <ScanSection isLoggedIn={isLoggedIn} />
      </div>
    </>
  );
}
export default Home;
