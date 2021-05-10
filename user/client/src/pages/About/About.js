import React from "react";
import "./About.css";

import Emilia from "../../assets/emilia.jpg";
import Noah from "../../assets/noah.png";
import Aviel from "../../assets/aviel.png";
import Card from "../../components/Card/ProfileCard";
import cursive from "../../assets/cursive_trans.png";

function AboutSection() {
  return (
    <section className="about" id="about">
      <h3>About the project</h3>
      <div className="about-content">
        <div className="about-text-holder">
          <p>
            When an image is uploaded and scanned the system will return its predicted value. The system does it by spliting the image into two single paged images (if the image contains 2 pages),
            then it divide the image into small resolutions patches.
          </p>
          <p>
            Next, the system applies binarization on these patches to filter unwanted areas of the original image. The system filters the areas that contain noisy data (salt and pepper) and plain
            colored areas without text, based on the ratio between the black and the white pixels. After the filtering, the corresponding original patches are saved in grayscale and used to predict
            the script.
          </p>
          <p>After the filtering is done the corresponding orignal patches are saved in grayscale and used to predict the origin and the shape of the script.</p>
        </div>
        <div className="image-rotate-holder">
          <img className="rotating-image" alt="something" src={cursive}></img>
        </div>
      </div>
    </section>
  );
}
function WWASection() {
  return (
    <section className="wwa" id="wwa">
      <h3>Who we are</h3>
      <p>
        We are fourth year students of Software Engineer department at SCE. During the summer time and the first semester we researched and experimented with different models and architectures, and
        strove for high accuracies. This project was completed disregarding the challenges and limitations imposed on us by the Covid19 outbreak in 2020.
      </p>
      <p>
        During the second semester we shifted towards developing the website that will provide researchers with automatic recognition of Hebrew scripts and script sub-types. Our main focus was to
        develop strong functionality from front to back. We combined RESTful api to handle requests, JWT for token authentication and Redis for cache and token whitelisting, and developed a secure
        login and registration. Additionally, we made sure that our website will be functional and responsive on different devices and resolutions.
      </p>
      <div className="cards-holder">
        <Card name={"Noah Solomon"} image={Noah} github_link={"https://github.com/SoloNoah"} linkedin_link={"https://www.linkedin.com/in/noah-solo/"} />
        <Card name={"Emilia Zorin"} image={Emilia} github_link={"https://github.com/EmiliaZorin"} linkedin_link={"https://www.linkedin.com/in/emilia-zorin/"} />
        <Card name={"Aviel Cohen"} image={Aviel} github_link={"https://github.com/AvielCo"} linkedin_link={"https://www.linkedin.com/in/AvielCo/"} />
      </div>
    </section>
  );
}
function About({ isLoggedIn, setIsLoggedIn }) {
  return (
    <React.Fragment>
      <AboutSection />
      <WWASection />
    </React.Fragment>
  );
}

export default About;
