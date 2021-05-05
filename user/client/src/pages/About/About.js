import React from 'react';
import './About.css';

import { NavBar } from '../../components';
import Emilia from '../../assets/emilia.jpg';
import Noah from '../../assets/noah.png';
import Aviel from '../../assets/aviel.png';
import Card from '../../components/Card/ProfileCard';
import cursive from '../../assets/cursive_trans.png';

function AboutSection() {
  return (
    <section className='about' id='about'>
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
    <section className='wwa' id='wwa'>
      <h3>Who we are</h3>
      <p>
        We are 4th year Software Engineering students at SCE Sami Shamoon. We decided to join Dr. Irina Rabaev and with her guidance tackle this challenge. During summer time and the first semester we
        researched and experimented with different models and architectures and strive for high accuracies with the limitations and the challenges presented to us during the Covid outbreak in 2020.
      </p>
      <p>
        In the second semester we shifted towards developing the website that will allow paleographers to easily classify hebrew scripts with ease. We focused on developing strong functionality from
        front to back. Combining RESTapi to handle requests and JWT we developed a secure login and registration. Additionally, we made sure that our website will be functional and responsive on
        different devices and resolutions
      </p>
      <div className='cards-holder'>
        <Card name={'Noah Solomon'} image={Noah} github_link={'https://github.com/SoloNoah'} linkedin_link={'https://www.linkedin.com/in/noah-solo/'} />
        <Card name={'Emilia Zorin'} image={Emilia} github_link={'https://github.com/EmiliaZorin'} linkedin_link={'https://www.linkedin.com/in/emilia-zorin/'} />
        <Card name={'Aviel Cohen'} image={Aviel} github_link={'https://github.com/AvielCo'} linkedin_link={'https://www.linkedin.com/in/AvielCo/'} />
      </div>
    </section>
  );
}
function About() {
  return (
    <React.Fragment>
      <NavBar />
      <AboutSection />
      <WWASection />
    </React.Fragment>
  );
}

export default About;
