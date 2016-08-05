import React from "react";
import { Link } from "react-router";

import Footer from "../components/Layout/Footer.jsx";
import Nav from "../components/Layout/Nav.jsx";

export default class Layout extends React.Component {
  render() {
    const { location } = this.props;
    const containerStyle = {
        marginTop: "60px",
        paddingBottom: "10px"
    };

    return (
      <div>
        <Nav location={location} />

        <div class="container" style={containerStyle}>
          <div class="row">
            <div class="col-lg-12">
                {this.props.children}
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}