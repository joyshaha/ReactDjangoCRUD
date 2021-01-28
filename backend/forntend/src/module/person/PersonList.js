import React, { Component } from "react";
import { Table } from "reactstrap";
import NewPersonModal from "./NewPersonModal";
import RemovePersonModal from "./RemovePersonModal";

class PersonList extends Component {
  render() {
    const persons = this.props.persons;
    return (
      <Table  className='shadow'>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Birthdate</th>
            <th>Location</th>
            <th className='text-center'>Action</th>
          </tr>
        </thead>
        <tbody>
          {!persons || persons.length <= 0 ? (
            <tr>
              <td colSpan="6" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            persons.map(person => (
              <tr key={person.id}>
                <td>{person.name}</td>
                <td>{person.email}</td>
                <td>{person.birth_date}</td>
                <td>{person.location}</td>
                <td align="center">
                  <NewPersonModal
                    create={false}
                    person={person}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <RemovePersonModal
                    pk={person.id}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default PersonList;