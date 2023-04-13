import React, { useEffect, useState } from "react";
import "./Form.css";
import Shauryam from "../shauryam.jpg"

function Form() {
  const [data, setData] = useState([]);
  useEffect(() => {
    var headers = new Headers();
    // headers.append("Content-Type", "application/json");
    // headers.append("Access-Control-Allow-Origin","*")
    let params = {
      method: "GET",
      // headers:headers,
      redirect: "follow",
    };
    fetch("http://localhost:5000/get_image", params)
      .then((res) => res.json())
      .then((response) => {
        console.log(response);
        setData(response.data[0]);
      });
  }, []);
  function handleSubmit(e) {
    e.preventDefault()
    console.log("YO");
    console.log(e.target.name.value)
    const result = new FormData();
    result.append("name", document.getElementById("name"));
    result.append("details", document.getElementById("details"));
    let params = {
      method: "POST",
      body: result,
    };
    fetch("http://localhost:5000/add_user", params)
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      });
  }
  return (
    <div>
      { (
        <>
          <div className="profileImage">
            <img src={}/>
          </div>
          <h1 className="basicDetails">BASIC DETAILS</h1>
          <form
            className="formContainer"
            name="detailForm"
            onSubmit={handleSubmit}
          >
            <div>
              <label for="name">Name: </label>
              <input
              id="name"
                className="formEntry"
                type="text"
                name="name"
                placeholder="Enter Your Name"
              />
            </div>
            <div>
              <label for="name">Phone Number: </label>
              <input
                className="formEntry"
                type="number"
                name="details"
                placeholder="Enter Your Phone Number"
              />
            </div>
            <div>
              <label for="name">Address: </label>
              <input
              id="details"
                className="formEntry"
                type="text"
                name="address"
                placeholder="Enter Your Address"
              />
            </div>
            <button type="submit" className="submitButton" style={{margin:"36px"}}>
              Submit
            </button>
          </form>
        </>
      )}
    </div>
  );
}

export default Form;
