import React from "react";
import {Button, Form, FormGroup, Input, Label} from "reactstrap";

import axios from "axios";

import {API_URL_PERSON} from "../../constants";

class NewPersonForm extends React.Component {
    state = {
        id: 0,
        name: "",
        email: "",
        birth_date: "",
        location: ""
    };

    componentDidMount() {
        if (this.props.person) {
            const {id, name, birth_date, email, location} = this.props.person;
            this.setState({id, name, birth_date, email, location});
            console.log(id, name, birth_date, email, location)
        }
    }

    onChange = e => {
        this.setState({[e.target.name]: e.target.value});
    };

    createPerson = e => {
        e.preventDefault();
        axios.post(API_URL_PERSON, this.state).then(() => {
            //console.log(this.state);
            this.props.resetState();
            this.props.toggle();
        });
    };

    editPerson = e => {
        e.preventDefault();
        axios.put(API_URL_PERSON + this.state.id, this.state).then(() => {
            //console.log(this.state.id);
            this.props.resetState();
            this.props.toggle();
        });
    };

    defaultIfEmpty = value => {
        return value === "" ? "" : value;
    };

    render() {
        return (
            <Form onSubmit={this.props.person ? this.editPerson : this.createPerson}>
                <FormGroup>
                    <Label for="name">Name:</Label>
                    <Input
                        type="text"
                        name="name"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.name)}
                    />
                </FormGroup>
                <FormGroup>
                    <Label for="email">Email:</Label>
                    <Input
                        type="email"
                        name="email"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.email)}
                    />
                </FormGroup>
                <FormGroup>
                    <Label for="birth_date">Birth Date:</Label>
                    <Input
                        type="text"
                        name="birth_date"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.birth_date)}
                    />
                </FormGroup>
                <FormGroup>
                    <Label for="location">Location:</Label>
                    <Input
                        type="text"
                        name="location"
                        onChange={this.onChange}
                        value={this.defaultIfEmpty(this.state.location)}
                    />
                </FormGroup>
                <Button>Send</Button>
            </Form>
        );
    }
}

export default NewPersonForm;