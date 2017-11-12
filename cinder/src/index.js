import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import { Navbar, Jumbotron, Button } from 'react-bootstrap';

class Square extends React.Component {
  render() {
    return (
      <div>
      <h2>Hello, world</h2>
      <p>This is Cinder</p>
      <Jumbotron>
      <Button bsStyle="primary" bsSize="large">Large button</Button>
      <Button bsSize="large">Large button</Button>
      </Jumbotron>
      </div>
         
     
    );
  }
}

ReactDOM.render(
  <Square />,
  document.getElementById('root')
);
