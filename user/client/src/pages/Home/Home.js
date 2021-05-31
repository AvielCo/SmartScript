import React, { useState } from "react";
import { ResultTextView } from "../../components";
import pic from "../../assets/landing-bg.jpg";
import { toast } from "react-toastify";
import axios from "axios";
import { getAccessToken } from "../../helpers";
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
  });

  const handleImageChange = async (event) => {
    event.preventDefault();
    if (event.target.files && event.target.files[0]) {
      setSelectedImage(event.target.files[0]);
      setImageUri(URL.createObjectURL(event.target.files[0]));
      setResult({
        success: false,
      });
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
      .post(`${process.env.REACT_APP_API_ADDRESS}/api/predict`, fd, getAccessToken() ? cfg : { headers: { "content-type": "multipart/form-data" } })
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
          toast.error("Please try again with different image.");
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
          {!isLoggedIn && (
            <p className="consider-log-in">
              Please consider signing up to save previous uploads for future use. <br /> This will take less than a minute.
            </p>
          )}
          <input accept="image/*" onChange={handleImageChange} id="upload-button" type="file" style={{ display: "none" }} disabled={isLoading} />
          <label htmlFor="upload-button">
            <Button className="scan-btn" component="span" name={"Upload"} disabled={isLoading} />
          </label>
          <Button className="scan-btn" type="submit" name={"Predict"} disabled={isLoading || !selectedImage}></Button>

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

function Home({ isLoggedIn }) {
  return (
    <div className="home" id="home">
      <LandingSection />
      <ScanSection isLoggedIn={isLoggedIn} />
    </div>
  );
}
export default Home;
