import React, { useState, useEffect } from "react";
import ClubDisplayContent from './clubDisplayHelpers/ClubDisplay'
import ClubPreview from './clubDisplayHelpers/ClubPreview'
import { useParams } from 'react-router-dom';

import axiosInstance from '../axios';

export default function Club() {

    const { id } = useParams();
    const [userAuth, setUserAuth] = useState(null);

    useEffect(() => {
      axiosInstance.get('user-auth-detail/' + id + '/')
      .then((response) => {
        setUserAuth(response.data.rank);
        })
      .catch((e) => {
        setUserAuth(e.response.data.detail);
      });
    }, [setUserAuth]);

    console.log(userAuth)

    return (
        <>
        {userAuth == 'Not found.' &&
          <ClubPreview/>
        }
        {userAuth == 'applicant' &&
          <ClubPreview/>
        }
        {userAuth != null &&
          <ClubDisplayContent/>
        }
        </>
    );
}