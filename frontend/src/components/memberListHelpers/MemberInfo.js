import React from "react";
import { makeStyles, Container, Card, CardActionArea, CardMedia, CardContent, Typography, CardActions, Button } from "@material-ui/core";
import { useNavigate, Link } from "react-router-dom";


import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import Parragraph2 from '../clubDisplayHelpers/Parragraph2'

const useStyles = makeStyles((theme) => ({
    card:{
        marginBottom:theme.spacing(5)
    },
}));




const MemberInfo = (props) => {

    const { members } = props;
    const classes = useStyles();

    if (!members || members.length === 0) return <p> No posts made yet!</p>;
    return (
        <React.Fragment>
    {members.map((member) => {
    return ( 
    <ListItem
            key={member.user}
              disablePadding
            >
              <ListItemButton dense>

                <Parragraph2>
                {member.user}
                </Parragraph2>
              </ListItemButton>
            </ListItem>
    );
    })}
    </React.Fragment>
    );
};

export default MemberInfo;