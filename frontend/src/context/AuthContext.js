import React, { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import axiosInstance from "../axios";

const AuthContext = createContext()

export default AuthContext;


export const AuthProvider = ({children}) => {

    let [authTokens, setAuthTokens] = useState(()=> localStorage.getItem('access_token') ? (localStorage.getItem('access_token')) : null)
    let [user, setUser] = useState(()=> localStorage.getItem('access_token') ? jwt_decode(localStorage.getItem('access_token')) : null)
    let [loading, setLoading] = useState(true)
    let [clubOwner, SetIsOwner] = useState()

    let checkOwner = (club_id) => {
        axiosInstance.get('get-owner/' + club_id + '/').then((res) => {
            if(res.data.user==user.username) {
                SetIsOwner(user)
                console.log(res.data.user)
            }
        }
        )
    }


   



    let contextData = {
        user:user,
        authTokens:authTokens,
        setAuthTokens:setAuthTokens,
        setUser:setUser,
        clubOwner:clubOwner,
        
    }

    useEffect(()=> {

        if(authTokens){
            setUser(jwt_decode(authTokens))
        }
        // else{
        //     setUser(null)
        // }
        setLoading(false)


    }, [authTokens, loading])




    return(
        <AuthContext.Provider value={contextData}>
            {loading ? null: children}
        </AuthContext.Provider>
    )
}