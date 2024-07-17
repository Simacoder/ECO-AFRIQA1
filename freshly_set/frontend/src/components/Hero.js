import React from 'react'
import "./Hero.css"
function Hero() {
  return (
    <div className="heroBg">

        <div className="heroComps">
            {/* <img className="bgSm" src="/images/small_bg.png"/> */}
        {/* <div className="heroTest"></div> */}

            <h1 className="font-inter">Urbanization Farming and    
            Vertical Farming</h1>

            <h2 className="font-bold">Freshly Farms is known for urbanizing the food farming industry especially on horticulture. It helps farmers understand their crops and how to manage them to grow better</h2>
                <div className="heroBtn">
                    <button>GET STARTED</button>

                </div>
            <div className="">
                {/* <img className="heroImgBg" src="/images/heroImage.png" alt="HeroImg"/> */}
                <img className="heroImgBg" src={`static/media/heroImage.png`} alt="HeroImg" />


            </div>

                <img className="heroImg" src={`static/media/HeroImg.png`} alt="Hero img"/>


          
        </div>

    </div>
  )
}

export default Hero