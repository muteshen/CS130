/*
  Name: Swipe
  Purpose: Main page that allows users to click (swipe) left or right to
           indicate their preference towards potential dates
  Author: Ryan Stenberg
*/

/*
  User Experience:
    1. Profile of potential date is center screen
    2. Swipe left for no | Swipe right for yes (swipe = click on desktop)
    3. Either swipe causes next date to pop up

  Implementation:
    1. Queue of user profiles
      - Store 20 users in queue, request 10 more when queue hits size 10
    2. Only ask for minimum data
      - Name
      - Bio
      - Picture
      - Age
      - Location
    3.
*/

import React from 'react';

class Swipe extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      // States here
    }
  }

  render() {
    <h1>This is the swipe page</h1>
  }
}
