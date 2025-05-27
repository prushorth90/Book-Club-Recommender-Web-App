import React, { Component, useEffect } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";
import CreateClubPage from "./CreateClubPage";
import LoginPage from "./accounts/Login";
import Logout from "./accounts/Logout";
import SignUpPage from "./accounts/SignUpPage";
import Club from "./Club";
import Dashboard from "./Dashboard";
import { 
  BrowserRouter as Router,
  Routes, 
  Route,
  Link,
  Redirect
  } from "react-router-dom";
import UpdateProfile from "./UpdateProfile";
import UpdatePassword from "./UpdatePassword";
import MyClubs from "./MyClubs";
import CreateMeeting from "./CreateMeeting";
import CreatePost from "./CreatePost";
import ShowMeeting from "./ShowMeeting";
import UpdateMeeting from "./UpdateMeeting";
import ApplicantList from './ApplicantList';
import MemberList from './MemberList';
import RateBooks from "./RateBooks";
import ChatRoom from "./ChatRoom";
import PrivateRoute from "./common/PrivateRoute";
import PrivateRoute2 from "./common/PrivateRoute2";
import { AuthProvider } from "../context/AuthContext";

function App(){
    return (
      <Router style={{backgroundColor: 'blue',}}>
        <AuthProvider>
            <Routes>
                <Route path ="/" exact element={<HomePage/>}></Route>
                <Route path ="/signup" element={<SignUpPage/>}></Route>
                <Route path ="/login" element={
                    <LoginPage/>
                }></Route>
                <Route path ="/rate_books" element={
                <PrivateRoute>
                <RateBooks/>
                </PrivateRoute>

                }></Route>

                <Route path ="/club/:id/chat-room" element={<ChatRoom/>}></Route>

                <Route path ="/logout" element={
                <Logout/>
                }></Route>
                <Route path ="/update_profile" element={
                <PrivateRoute>
                <UpdateProfile/>
                </PrivateRoute>
                
                }></Route>
                <Route path ="/update_password" element={
                <PrivateRoute>
                <UpdatePassword/>
                </PrivateRoute>
              }></Route>

                <Route path ="/dashboard" element={
                <PrivateRoute>
                <Dashboard/>
                </PrivateRoute>
                }>
                </Route>
                <Route path ="/create" element={
                <PrivateRoute>
                <CreateClubPage/>
                </PrivateRoute>

                }></Route>
                <Route path ="/club/:id" element={
                <PrivateRoute>
                <Club/>
                </PrivateRoute>
                }></Route>

                <Route path ="/my_clubs" element={
                <PrivateRoute>
                <MyClubs/>
                </PrivateRoute>

                }></Route>


                <Route path ="/applicant_list/:id" element={
                <PrivateRoute>
                <ApplicantList/>
                </PrivateRoute>

                }></Route>
                <Route path ="/member_list/:id" element={
                <PrivateRoute>
                <MemberList/>
                </PrivateRoute>
                }></Route>
                

                <Route path ="/create-post/:id" element={
                <PrivateRoute>
                <CreatePost/>
                </PrivateRoute>
                }></Route>

                <Route path ="/create_meeting/:id" element={
                <PrivateRoute>
                <CreateMeeting/>
                </PrivateRoute>

                }></Route>
                <Route path ="/show_meeting/:id" element={
                  <PrivateRoute>
                <ShowMeeting/>
                </PrivateRoute>
                }></Route>
                <Route path ="/update_meeting/:id" element={
                <PrivateRoute>
                <UpdateMeeting/>
                </PrivateRoute>
                }></Route>
            </Routes>
            </AuthProvider>
        </Router>
        );
    };  


const appDiv = document.getElementById("app");
render(<App />, appDiv);

export default App;