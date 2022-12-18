import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

class Intro extends React.Component {
    render() {
      return (
        <h1>Hello REACT!</h1>
      );
    }
  }

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Intro />);