import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';

function Subtitle(props) {
  return (
    <Typography component="h2" variant="h3" color="#7f4820" gutterBottom>
      {props.children}
    </Typography>
  );
}

Subtitle.propTypes = {
  children: PropTypes.node,
};

export default Subtitle;