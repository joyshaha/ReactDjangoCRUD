import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import PersonList from "./PersonList";
import NewPersonModal from "./NewPersonModal";

import axios from "axios";

import { API_URL_PERSON } from "../../constants";


class Person extends Component {
  state = {
    persons: []
  };

  componentDidMount() {
    this.resetState();
  }

  getPersons = () => {
    axios.get(API_URL_PERSON).then(res =>this.setState({ persons: res.data }));
  }; 

  resetState = () => {
    this.getPersons();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <PersonList
              persons={this.state.persons}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <NewPersonModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Person;