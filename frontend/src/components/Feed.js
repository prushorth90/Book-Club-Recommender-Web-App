import React from "react";
import { makeStyles, Container} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    container:{
        paddingTop: theme.spacing(10),
    }
}));

const Feed = () => {
    const classes = useStyles();
    return (
         <Container className ={classes.container}>feed </Container>
    );
};

export default Feed;