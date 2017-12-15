/*  Name:   meet.js
 *  Author: Ryan Stenberg
 *  Purpose: Functions to to called by elements in meet.html
 */

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

    // Get initial users
    var getUsersRequest = new XMLHttpRequest()
    getUsersRequest.onreadystatechange = function() {
      if (getUsersRequest.readyState == XMLHttpRequest.DONE && getUsersRequest.status == 200) {
        console.log('Retrieved first set of users.')

        // Parse response into JSON
        const responseText = getUsersRequest.responseText
        const responseJSON = JSON.parse(responseText)

        // Parse response JSON to get users
        const userArr = JSON.parse(responseJSON.result)
        for (var i = 0; i < userArr.length; i++) {
          const user = userArr[i]
          upcomingUsers.push(user)
        }
        setNextUserAsCurrent()
      }
    }
    const url = '/api/getUsers'
    getUsersRequest.open("GET", url)
    getUsersRequest.send()
  }

  /* Author: Ryan Stenberg
   * Parameters: num = Number of users to get
   * Returns: N/A
   * Notes: Fills upcomingUsers array with next num users in the local area
   *        Swipe right means user is interested
   */
  const getNextUsers = () => {
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = () => {
      if (this.readyState == 4 && this.status == 200) {
        const response = this.responseText
        const userJson = JSON.parse(response)
        for (user in userJson) {
          upcomingUsers.push(userJson[user])
        }
      }
    }
    const url = '/api/getUsers'
    xhttp.open("GET", url)
    xhttp.send()
  }

  const fillUserQueue = () => {
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
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
        const response = xhttp.responseText
        if (response != null) {
          match = JSON.parse(JSON.parse(response))
          console.log('Match found!')
          console.log(match)
          showModal(match)
        }
      }
    }
    const url = '/api/swipe'
    const jsonStr = JSON.stringify({
      id: `${currentPotentialMatch._id.$oid}`,
      like: dir === 'right' ? 'True' : 'False',
    })
    xhttp.open("POST", url)
    xhttp.setRequestHeader('content-type', 'application/json')
    xhttp.send(jsonStr)

    setNextUserAsCurrent()

    if (upcomingUsers.length < 4)
      fillUserQueue()
  }

  const setProfilePic = (id, forModal=false) => {

    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
        const response = xhttp.responseText

        if (response) {
          console.log('Received Image')
          if (forModal)
            matchPic.src = `data:image/jpeg;base64,${response}`
          else
          profilePic.src = `data:image/jpeg;base64,${response}`
        }
      }
    }
    const url = '/api/getPicture'
    const jsonStr = JSON.stringify({
      uid: `${id}`,
    })
    xhttp.open('POST', url)
    xhttp.setRequestHeader('content-type', 'application/json')
    xhttp.send(jsonStr)
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
      rightChevron.classList.remove('glyphicon-chevron-invalid')
      leftChevron.classList.remove('glyphicon-chevron-invalid')
      rightChevron.classList.add('glyphicon-chevron-valid')
      leftChevron.classList.add('glyphicon-chevron-valid')

      name.innerHTML = currentPotentialMatch.profile.first + ' ' + currentPotentialMatch.profile.last
      age.innerHTML = currentPotentialMatch.profile.age
      bio.innerHTML = currentPotentialMatch.profile.bio
      location.innerHTML = currentPotentialMatch.profile.location
      setProfilePic(currentPotentialMatch._id.$oid)
    } else {
      rightChevron.classList.remove('glyphicon-chevron-valid')
      leftChevron.classList.remove('glyphicon-chevron-valid')
      rightChevron.classList.add('glyphicon-chevron-invalid')
      leftChevron.classList.add('glyphicon-chevron-invalid')
    }
  }

  /* Author: Ryan Stenberg
   * Parameters: matchedUser = user object that has been successfully matched
   * Returns: N/A
   * Notes: Displays the modal after inserting new match's user data
   */
  const showModal = (matchedUser) => {
    matchName.innerHTML = matchedUser.profile.first + ' ' + matchedUser.profile.last
    setProfilePic(matchedUser._id.$oid, forModal=true)
    console.log('Showing match modal')
    $("#myModal").modal("show")
  }

  /* Author: Ryan Stenberg
   * Parameters: N/A
   * Returns: N/A
   * Notes: Hides the modal
   */
  const hideModal = () => {
    match = {}
    $("#myModal").modal("hide")
  }
  closeModalButton.addEventListener('click', hideModal)

  initialize()
}
