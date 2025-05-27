import React, { useEffect, useState } from "react";
import { makeStyles, Container} from "@material-ui/core";
import { useParams, Navigate} from "react-router-dom";
import axiosInstance from '../axios';
import List from '@mui/material/List';
import MemberInfo from "./memberListHelpers/MemberInfo";
import MemberInfoLoadingComponent from "./memberListHelpers/MemberInfoLoading";
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

const MemberList = () => {


    const [userAuth, setUserAuth] = useState(null);
    const { id } = useParams();
    const MemberInfoLoading = MemberInfoLoadingComponent(MemberInfo);
    const [appState, setAppState] = useState({
        loading: false,
        members: null,
    });

    useEffect(() => {
        setAppState({ loading: true });
        axiosInstance.get('member-list/'+id+'/').then((res) => {
            setAppState({ members: res.data, loading: false });
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
    return(
        <>
        {userAuth == 'Not found.' &&
          <Navigate to={"/club/"+id}/>
        }
         {userAuth == 'applicant.' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'member' &&
        <div>
            <Container className ={classes.container}>
                <Template/>
            <Title>Members</Title>
                <Parragraph>Here is a list with all of the members of the Clubs</Parragraph>
                <List component="nav">
                    <MemberInfoLoading isLoading={appState.loading} members={appState.members} />
                </List>
            </Container>
        </div>
}
        {userAuth == 'owner' &&
        <div>
            <Container className ={classes.container}>
                <Template/>
            <Title>Members</Title>
                <Parragraph>Here is a list with all of the members of the Clubs</Parragraph>
                <List component="nav">
                    <MemberInfoLoading isLoading={appState.loading} members={appState.members} />
                </List>
            </Container>
        </div>
}
        </>
    )
};

export default MemberList;
