/*  Name:   meet.js
 *  Author: Ryan Stenberg
 *  Purpose: Functions to to called by elements in meet.html
 */

// Only needed for testing
/********************** DUMMY DATA START **************************
const dummyUsers = [
  {
    id: 'ankfq214n5011',
    name: 'Selena',
    age: '24',
    bio: 'Hello my name is Selena. I live in west LA near Santa Monica. I work at a local coffee shop and moved here to be able to enjoy the beach, the warm weather, and all the sand that Los Angeles has to offer!',
    location: 'Los Angeles',
  },
  {
    id: 'f128nnkgg9918',
    name: 'Joan',
    age: '25',
    bio: 'Hello my name is Joan',
    location: 'Santa Barbara',
  },
  {
    id: '12nfs92bmz0ow',
    name: 'Sophia',
    age: '26',
    bio: 'Hello my name is Sophia',
    location: 'San Diego',
  },
  {
    id: '9os3nt099sk2a',
    name: 'Aliza',
    age: '27',
    bio: 'Hello my name is Aliza',
    location: 'San Francisco',
  },
  {
    id: 'mczn8201m2028',
    name: 'Claire',
    age: '28',
    bio: 'Hello my name is Claire',
    location: 'Los Gatos',
  },
]
********************** DUMMY DATA END ***************************/

window.onload = () => {

  /*****************************************************/
  /****************** Data Structures ******************/
  /*****************************************************/

  /* Container for next 20 users
    User: {
      name: String,
      age: Int,
      bio: String,
      currentCity: String,
    }
  */
  var upcomingUsers = []
  // upcomingUsers = dummyUsers  // Only needed for testing

  // Current user being looked at on Meet page
  var currentPotentialMatch = {}

  // Match if it currently exists (when modal is showing)
  var match = {}



  /*********************************************************/
  /*************** Event Listener Assignment ***************/
  /*********************************************************/

  // Tell chevrons to call handleSwipe on click
  var leftChevron = document.getElementById('chevron-left')
  var rightChevron = document.getElementById('chevron-right')
  if (leftChevron)
    leftChevron.addEventListener('click', () => handleSwipe('left'))
  if (rightChevron)
    rightChevron.addEventListener('click', () => handleSwipe('right'))

  var profilePic = document.getElementById('profile-pic')
  var name = document.getElementById('name')
  var age = document.getElementById('age')
  var bio = document.getElementById('bio')
  var location = document.getElementById('location')

  var modal = document.getElementById('myModal')
  var matchName = document.getElementById('match-name')
  var matchPic = document.getElementById('match-pic')
  var closeModalButton = document.getElementById('close-modal')



  /*****************************************************/
  /********************* Functions *********************/
  /*****************************************************/

  /* Author: Ryan Stenberg
   * Parameters: N/A
   * Returns: N/A
   * Notes: Run when page loads. Attempt to get user's current location and
   *        then get info for first 30 users in the area
   */
  const initialize = () => {
      console.log("Initializing...")
      console.log("Getting current location")
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setCoords)
      } else {
        console.error("Geolocation is not supported by this browser.")
      }
  }

  /* Author: Ryan Stenberg
   * Parameters: position = object with property coords { latitude, longitude }
   * Returns: N/A
   * Notes: 1. Called by success callback of getCurrentPosition()
   *        2. Sets local "coords" storage to contain user's coordinates
   *        3. Attempts to get first 30 potential matches
   */
  const setCoords = (position) => {
    const { latitude, longitude } = position.coords
    console.log(`Setting coordinates of current user to (${latitude},${longitude})`)

    if (latitude && longitude) {
      var xhttp = new XMLHttpRequest()
      xhttp.onreadstatechange = () => {
        if (this.readyState == 4 && this.status == 200) {
          console.log(this.responseText)
          console.log('Update profile coordinates successful.')

          // Get users
          var xhttp = new XMLHttpRequest()
          xhttp.onreadstatechange = () => {
            if (this.readyState == 4 && this.status == 404) {
              console.log('Retrieved first set of users.')
              const response = this.responseText
              const userJson = JSON.parse(response)
              for (user in userJson) {
                upcomingUsers.push(userJson[user])
              }
              setNextUserAsCurrent()
            }
          }
          const url = '/getUsers'
          xhttp.open("GET", url)
          xhttp.send()

        } else if (this.status == 404) {
          console.error('404: Could not send location.')
        }
      }
      const url = '/api/updateProfile'
      const jsonStr = JSON.stringify({location: `${latitude},${longitude}`})
      xhttp.open('POST', url)
      xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8')
      xhttp.send(jsonStr)
    }

    // Temporary placeholder
    // console.log(latitude, longitude)
  }

  /* Author: Ryan Stenberg
   * Parameters: num = Number of users to get
   * Returns: N/A
   * Notes: Fills upcomingUsers array with next num users in the local area
   *        Swipe right means user is interested
   */
  const getNextUsers = () => {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadstatechange = () => {
      if (this.readyState == 4 && this.status == 200) {
        const response = this.responseText
        const userJson = JSON.parse(response)
        for (user in userJson) {
          upcomingUsers.push(userJson[user])
        }
      }
    }
    const url = '/getUsers'
    xhttp.open("GET", url)
    xhttp.send()
  }

  const fillUserQueue = () => {
    // Fill queue to 10-15 users
    const numCalls = 2 - (upcomingUsers.length / 5)
    for (var i = 0; i < numCalls; i++)
      getNextUsers() // Always retrieves 5 users
  }

  /* Author: Ryan Stenberg
   * Parameters: dir = Direction that user swiped.
   * Returns: N/A
   * Notes: Swipe left means user is not interested
   *        Swipe right means user is interested
   */
  const handleSwipe = (dir) => {
    if (dir !== 'left' && dir !== 'right')
      console.error('Invalid swipe direction.')

    var xhttp = new XMLHttpRequest()
    xhttp.onreadstatechange = () => {
      if (this.readyState == 4 && this.status == 200) {
        const response = this.responseText
        const json = JSON.parse(response)
        if (json.isMatch) {
          match = {
            id: json.id,
            profile: json.profile,
          }
          showModal(match)
        }
      }
    }
    const url = "users/..."
    const jsonStr = JSON.stringify({
      id: `${currentPotentialMatch.id}`,
      like: `${dir === 'right' ? true : false}`,
    })
    xhttp.open("POST", url)
    xhttp.send(jsonStr)

    // Temporary placeholder
    // if (dir === 'right') showModal(currentPotentialMatch)

    setNextUserAsCurrent()

    if (upcomingUsers.length < 4)
      fillUserQueue()
  }

  /* Author: Ryan Stenberg
   * Parameters: N/A
   * Returns: N/A
   * Notes: loads the next user from the queue and makes them visible to client
   */
  const setNextUserAsCurrent = () => {
    const nextUser = upcomingUsers.splice(0,1)
    if (nextUser.length === 1) {
      currentPotentialMatch = nextUser[0]

      // profilePic.innerHTML = currentPotentialMatch.profilePic
      name.innerHTML = currentPotentialMatch.profile.name
      age.innerHTML = currentPotentialMatch.profile.age
      bio.innerHTML = currentPotentialMatch.profile.bio
      location.innerHTML = currentPotentialMatch.profile.location
    }
  }

  /* Author: Ryan Stenberg
   * Parameters: matchedUser = user object that has been successfully matched
   * Returns: N/A
   * Notes: Displays the modal after inserting new match's user data
   */
  const showModal = (matchedUser) => {
    // matchPic = matchedUser.pic
    console.log(matchedUser)
    matchName.innerHTML = matchedUser.profile.name
    $("#myModal").modal("show")
  }

  /* Author: Ryan Stenberg
   * Parameters: N/A
   * Returns: N/A
   * Notes: Hides the modal
   */
  const hideModal = () => {
    // Code to make modal hidden
    match = {}
    $("#myModal").modal("hide")
  }
  closeModalButton.addEventListener('click', hideModal)

  // initialize the page on window load
  initialize()
}
