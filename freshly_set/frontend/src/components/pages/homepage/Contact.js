import React from "react";
import { AiFillTwitterCircle } from "react-icons/ai";
import { FaTiktok } from "react-icons/fa6";

function Contact() {
  return (
    <div className="block lg:flex w-[100%] justify-between">
      <div className="mt-[132px] ml-[40px] block space-y-[29px]">
        <div className="flex justify-between lg:w-[478px]">
          <div classsName="block">
            <img
              className="h-[49px] w-[45px]"
              src="/static/media/mail.svg"
              alt="email"
            />
            <p className="font-[720] text-[72] -mt-[5px] font-inter">Email</p>
            <a href="mailto:info@freshlyfarms" className="font-normal no-underline" target="_blank">
              <p className="font-[22] text-[400] text-[#525560] font-josefin -mt-[10px]">info.freshlyfarms5@gmail.com</p>
            </a>
          </div>

          <div classsName="block -ml-[30px]">
            <img
              className="h-[49px] w-[45px]"
              src="/static/media/call.svg"
              alt="phone"
            />
            <p className="font-[720] text-[72] -mt-[5px] font-inter ">Phone</p>
            <p className="font-[22] text-[400] text-[#525560] font-josefin -mt-[10px]">
              {" "}
              +254 701 234 567{" "}
            </p>
          </div>
        </div>
        <div className="flex justify-between lg:w-[478px]">
          <div classsName="block">
            <img
              className="h-[49px] w-[45px]"
              src="/static/media/location.svg"
              alt="Office"
            />
            <p className="font-[720] text-[72] -mt-[5px] font-inter">Office</p>
            <p className=" font-josefin text-[#525560] font-[22] text-[400] -mt-[10px]">
              {" "}
              Nairobi, Kenya{" "}
            </p>
          </div>

          <div classsName="block ">
            <img
              className="h-[49px] w-[45px] ml-[20px]"
              src="/static/media/globe.svg"
              alt="Social Media"
            />
            <p className="font-[720] text-[72] -mt-[5px] font-inter ml-[20px]">Socials</p>
            <div className="flex items-center space-x-[5px]  ">
              <a href="" title="Instagram" target="_blank">
                <img
                  src="/static/media/instagram.svg"
                  className="h-[37px]  w-[32px]"
                />
              </a>

              <a
                href="https://www.facebook.com/profile.php?id=61561757183894"
                title="Facebook"
                target="_blank"
              >
                <img
                  src="/static/media/facebook.svg"
                  className="h-[37px]  w-[32px]"
                />
              </a>

              <a
                href="https://x.com/FreshlyFarms5"
                title="Twitter"
                target="_blank"
              >
                <img
                  src="/static/media/twitter.svg"
                  className="h-[37px]  w-[32px]"
                />
              </a>

              <a
                href="https://www.tiktok.com/@infofkexnoo?_t=8o7P91f39aI&_r=1"
                title="Tiktok"
                target="_blank"
              >
                <img
                  src="/static/media/tiktok.svg"
                  className="h-[37px]  w-[32px]"
                />
              </a>
            </div>
          </div>

    </div>
      </div>
      <div className="block mt-[94px] ml-[20px] lg:ml-[187px] lg:mr-[84px] ">
        <p className="text-[22px] text-black font-[700]">Email</p>
        <input
          placeholder="john@gmail.com"
          className="h-[46px] w-[308px] mx-auto lg:w-[474px] lg:h-[46px] py-[10px] px-[14px] rounded-[8px] border-solid border-[1px] border-[#D5DAE1] focus:outline-none"
        />
        <p className="font-inter text-[16px] font-[500] text-[#333F51]">
          Message
        </p>
        <textarea
          className="h-[220px] w-[332px] lg:h-[220px] lg:w-[474px]  rounded-[8px] border-solid border-[1px] border-[#D5DAE1] focus:outline-none"
          placeholder="Your message..."
        />

        <div className="lg:flex justify-center">
          <button className="h-[56px] w-[332px] rounded-[14px] bg-[#008000] border-none font-inter text-[25px]  text-white font-[700] mt-[41px]">Send</button>

        </div>
      </div>
    </div>
  );
}

export default Contact;
