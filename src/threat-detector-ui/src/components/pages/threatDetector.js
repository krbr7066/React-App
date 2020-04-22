import React, { Component } from 'react'
import {
  Button,
  Input,
  Footer,
  Card,
  CardBody,
  CardImage,
  CardTitle,
  CardText
} from "mdbreact";

import threats from "./threats.json";

class threatDetector extends Component {
    state = {
    search: ""
  };

  renderThreat = threatName => {
    const { search } = this.state;
    var threat_id = threatName.threat_id;

    return (
      <div className="col-md-3" style={{ marginTop: "20px" }}>
        <Card>
          <CardBody>
            <CardTitle title={threatName.name}>
              {threatName.name.substring(0, 15)}
              {threatName.name.length > 15 && "..."}
            </CardTitle>
          </CardBody>
        </Card>
      </div>
    );
  };

  onchange = e => {
    this.setState({ search: e.target.value });
  };

  render() {
    const { search } = this.state;
    const filteredCountries = threats.filter(threatName => {
      return threatName.name.toLowerCase().indexOf(search.toLowerCase()) !== -1;
    });

    return (
      <div className="flyout">
        <main style={{ marginTop: "4rem" }}>
          <div className="container">
            <div className="row">
             <h1 className="Filter threats by">Please sign in</h1>
              <div className="col">
                <Input
                  placeholder="Search Threat"
                  icon="search"
                  onChange={this.onchange}
                />

              </div>
              <div className="col" />
            </div>
            <div className="row">
              {filteredCountries.map(threatName => {
                return this.renderThreat(threatName);
              })}
            </div>
          </div>
        </main>
      </div>
    );
  }
}





export default threatDetector