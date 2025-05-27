import React, { useEffect, useState } from "react";
import { makeStyles, Container} from "@material-ui/core";
import { useParams, Navigate} from "react-router-dom";
import axiosInstance from '../axios';
import List from '@mui/material/List';
import ApplicantInfo from "./applicantListHelpers/ApplicantInfo";
import ApplicantInfoLoadingComponent from "./applicantListHelpers/ApplicantInfoLoading";
import Title from './clubDisplayHelpers/Title';
import Parragraph from './clubDisplayHelpers/Parragraph';
import Template from './Template'

const useStyles = makeStyles((theme) => ({
    container:{
        paddingTop: theme.spacing(10),
        overflow:"auto",
        maxHeight: 800,
    }
}));

const ApplicantList = () => {

    const { id } = useParams();
    const ApplicantInfoLoading = ApplicantInfoLoadingComponent(ApplicantInfo);
    const [appState, setAppState] = useState({
        loading: false,
        applicants: null,
    });

    useEffect(() => {
        setAppState({ loading: true });
        axiosInstance.get('applicant-list/'+id+'/').then((res) => {
            setAppState({ applicants: res.data, loading: false });
            console.log(res.data);
        });
    }, [setAppState]);

    useEffect(() => {
		axiosInstance.get('user-auth-detail/' + id + '/')
		.then((response) => {
		  setUserAuth(response.data.rank);
		  })
		.catch((e) => {
		  setUserAuth(e.response.data.detail);
		});
  
	  }, [setUserAuth]);

    const classes = useStyles();
    return (
        <>
        {userAuth == 'Not found.' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'applicant' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'member' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'owner' &&
        <div>
            <Container className ={classes.container}>
            <Template/>
                <Title>Applicants</Title>
                <Parragraph>Here is a list with all of the applicants of the Clubs</Parragraph>
                <List component="nav">
                    <ApplicantInfoLoading isLoading={appState.loading} applicants={appState.applicants} />
                </List>
            </Container>
        </div>
}
        </>
    )
};

export default ApplicantList;
