import React, { useEffect, useState }  from 'react'
import Template from './Template'
import { makeStyles, Button} from "@material-ui/core";
import { useNavigate, Link, Navigate } from "react-router-dom";
import axiosInstance from '../axios';
import { useParams} from "react-router-dom";
import { Container } from '@mui/material';



const useStyles = makeStyles((theme) => ({
  container:{
      paddingTop: theme.spacing(10),
      overflow:"auto",
      maxHeight: 800,
  }
}));


export default function ShowMeeting() {

  const { id } = useParams();
  const [data, setData] = useState({ meeting: [] });
  const [userAuth, setUserAuth] = useState(null);


  useEffect(() =>  {
      axiosInstance.get('meeting-detail/'+ id ).then((res) => {
          setData({ meeting: res.data });
          console.log(res.data);
          console.log(res.data.id);
      });
  }, [setData]);

  useEffect(() => {
		axiosInstance.get('user-auth-detail/' + id + '/')
		.then((response) => {
		  setUserAuth(response.data.rank);
		  })
		.catch((e) => {
		  setUserAuth(e.response.data.detail);
		});
  
	  }, [setUserAuth]);

  return (
    <>
    {userAuth == 'Not found.' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'applicant' &&
          <Navigate to={"/club/"+id}/>
        }
        {userAuth == 'member' &&
        <Container>
    <p> Bookname: {data.meeting.book} </p>
    <p> Club: {data.meeting.club} </p>
    <p> Creator: {data.meeting.creator } </p>
                    </Container>
}
        {userAuth == 'owner' &&
        <Container>
    <p> Bookname: {data.meeting.book} </p>
    <p> Club: {data.meeting.club} </p>
    <p> Creator: {data.meeting.creator } </p>
    <Link to={"/update_meeting/"+data.meeting.id}>
                        <Button size="small" style={{backgroundColor: "#21b6ae"}} >Info </Button>
                    </Link>
                    </Container>
}
    </>
  )
};
