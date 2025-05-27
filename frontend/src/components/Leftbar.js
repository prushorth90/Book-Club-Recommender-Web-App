import React from "react";
import { Container, makeStyles, Typography } from "@material-ui/core";
import { GroupAdd, Home } from "@material-ui/icons";
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
    container: {
        height: "100vh",
        color:"white",
        paddingTop: theme.spacing(10),
        backgroundColor: theme.palette.primary.main,
        position:"sticky",
        top: 0,
        [theme.breakpoints.up("sm")]:{
            backgroundColor:"white",
            color:"#555",
            border:"1px solid #ece7e7"
        },
    },
    item: {
        display:"flex",
        alignItems:"center",
        marginBottom: theme.spacing(4) ,
        [theme.breakpoints.up("sm")]:{
            marginBottom: theme.spacing(3),
            cursor:"pointer"
        },
    },
    icon : {
        marginRight: theme.spacing(1),
        [theme.breakpoints.up("sm")]:{
            fontSize:"18px",
        }
    },
    text: {
        fontWeight:500,
        [theme.breakpoints.down("sm")]:{
            display:"none",
        },
    },
    link: {
        textDecoration: "none",
        color:"#555"
    }
}));

const Leftbar = () => {
    const classes = useStyles();
    return (
    <Container className ={classes.container}>
        <Link to="/" className={classes.link}>
        <span className={classes.item}>
        <Home className={classes.icon} />
        <Typography className={classes.text}>Homepage</Typography>
      </span>
      </Link>
      <Link to="/create" className={classes.link}>
      <span className={classes.item}>
        <GroupAdd className={classes.icon} />
        <Typography className={classes.text}>Create Club</Typography>
      </span>
      </Link>
    </Container>
    );
};

export default Leftbar;