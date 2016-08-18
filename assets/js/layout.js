import React from 'react';
import { Grid, Row, Col, Well } from 'react-bootstrap';
import Tabs from './tabs';
import getStats from './stats-api';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.getQuery = this.getQuery.bind(this);
    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.toggleOpen = this.toggleOpen.bind(this);
    this.state = {
      open: false,
      query: {},
      count: 1913,
      userFilter: {
        user__total_n_classifications__gte: '',
        user__total_n_classifications__lte: '',
        user__talk_posts__gte: '',
        user__talk_posts__lte: '',
        user__survey_project__project__in: {
          GZ: true,
          PH: true,
          PW: true,
          SE: true,
          SS: true,
        },
        user__country__in: {
          US: true,
          UK: true,
          Ca: true,
          Au: true,
          Ge: true,
          Fr: true,
          Ne: true,
          Po: true,
          In: true,
        },
      },
    };
  }

  getQuery() {
    const surveyProject = [];
    for (const key in this.state.userFilter.user__survey_project__project__in) {
      if (this.state.userFilter.user__survey_project__project__in[key]) {
        surveyProject.push(key);
      }
    }
    const country = [];
    for (const key in this.state.userFilter.user__country__in) {
      if (this.state.userFilter.user__country__in[key]) {
        country.push(key);
      }
    }
    const query = {
      ...this.state.userFilter,
      user__survey_project__project__in: surveyProject,
      user__country__in: country,
    };
    // clean up unneeded querys
    if (surveyProject.length === 5) {
      delete(query.user__survey_project__project__in);
    }
    if (country.length === 9) {
      delete(query.user__country__in);
    }
    if (query.user__total_n_classifications__gte === '') {
      delete(query.user__total_n_classifications__gte);
    }
    if (query.user__total_n_classifications__lte === '') {
      delete(query.user__total_n_classifications__lte);
    }
    if (query.user__talk_posts__gte === '') {
      delete(query.user__talk_posts__gte);
    }
    if (query.user__talk_posts__lte === '') {
      delete(query.user__talk_posts__lte);
    }
    return query;
  }

  handleFilterChange(e) {
    if (e.target.type === 'checkbox') {
      const name = e.target.name.split('.');
      this.setState({
        userFilter: {
          ...this.state.userFilter,
          [name[0]]: {
            ...this.state.userFilter[name[0]],
            [name[1]]: e.target.checked,
          },
        },
      });
    } else {
      this.setState({
        userFilter: {
          ...this.state.userFilter,
          [e.target.name]: e.target.value,
        },
      });
    }
  }

  handleSubmit() {
    const query = this.getQuery();
    getStats(query, '1')
      .then((data) => (
        this.setState({
          count: data.count,
          query,
        })
      ));
  }

  toggleOpen() {
    this.setState({ open: !this.state.open });
  }

  render() {
    const filterProps = {
      open: this.state.open,
      toggleOpen: this.toggleOpen,
      handleChange: this.handleFilterChange,
      filterState: this.state.userFilter,
      onSubmit: this.handleSubmit,
      count: this.state.count,
    };
    return (
      <Grid>
        <Row>
          <Col xs={12}>
            <Well>
              Header goes here
            </Well>
          </Col>
        </Row>
        <Row>
          <Col xs={2}>
            <div className="sidebar">
              <Tabs />
            </div>
          </Col>
          <Col xs={10}>
            {React.cloneElement(this.props.children, { query: this.state.query, filterProps })}
          </Col>
        </Row>
      </Grid>
    );
  }
}

App.propTypes = {
  children: React.PropTypes.node,
};
