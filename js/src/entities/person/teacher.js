import { Link, useParams } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import { Row } from "react-bootstrap";
import { useEffect, useState } from "react";

import image from '../rozvrhSnimek.png'
import { DepartmentSmall } from "../group/department";


import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";
import { FacultySmall } from "../group/faculty";
import { GroupSmall } from "../group/group";
import { SubjectSmall } from "../studyprogram/subject";

export function TeacherSmall(props) {
    return (
        <Link to={root + "/users/teacher/" + (props.id)}>{props.name} {props.surname}</Link>
    )
}

export function TeacherMedium(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Vyučující - <TeacherSmall {...props} /></Card.Title>
            </Card.Header>
            <Card.Body>
                <Card.Text>
                    <b>Jméno příjmení:</b> {props.name} {props.surname}<br />
                    <b>Titul:</b> {props.degreeRank}<br />
                    <b>Katedra:</b> {props.departments}<br />
                    {/*<b>Fakulta:</b> {props.faculty}*/}
                </Card.Text>
            </Card.Body>
        </div>
    )
}

function ContactInfo(props) {
    //data=props.datas;
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Kontaktní údaje</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>E-mail:</b> {props.email}<br />
                <b>Telefon:</b> {props.phone ? props.phone : 'Neuvedeno'}<br />
                <b>Areál: </b> {props.areal}<br />
                <b>Budova: </b>{props.building} <b>Místnost:</b> {props.room}<br />
            </Card.Body>
        </div>
    )
}

const groupTypeComponent = {
    'fakulta': FacultySmall,
    'katedra': DepartmentSmall
}
export const GroupInfo = (props) => {
    const GroupLink = groupTypeComponent[props.grouptype.name] || GroupSmall
    return (
        <>
        <b>{props.grouptype.name}: </b>
        <GroupLink {...props} />
        <br />
        </>
    )
}

export const Membership = (props) => {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Členství</Card.Title>
            </Card.Header>
            <Card.Body>
                {props.groups.map((group, index) => (
                    <GroupInfo {...group} />
                ))}
            </Card.Body>
        </div>
    )
}

export function TeacherLarge(props) {
    

    const departments = []
    for (var index = 0; index < props.departments.length; index++) {
        if (index > 0) {
            departments.push(', ');
        }
        const sgItem = props.departments[index]
        departments.push(<DepartmentSmall {...props} id={sgItem.id} name={sgItem.name} key={sgItem.id} />);
    }

    return (
        <div className="card">
            <div className="card-header mb-3">
                <h4>Karta učitele</h4>
            </div>
            <div className="col">
                <Row>
                    <div className="col-3">
                        <TeacherMedium {...props} departments={departments} />
                        <ContactInfo {...props} />
                        <Membership {...props} />
                    </div>
                    <div className="col-6">
                        <RozvrhMedium />
                    </div>
                    <div className="col-3">
                        <SeznamPredmetu {...props} />
                    </div>
                </Row>
            </div>
        </div>
    )
}
/*
export function TeacherPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'lastname': props.lastname,
            'degreeRank': 'ing. plk.',
            "email": props.name.toLowerCase() + '.' + props.lastname.toLowerCase() + '1@unob.cz',
            'phone': '973 274 160',
            'areal': 'Kasárny Šumavská',
            'building': '5',
            'room': '104',
            'faculty': [
                { 'id': 23, 'name': 'FVT' }
            ],
            'departments': [
                { 'id': 1, 'name': 'K-209' },
                { 'id': 2, 'name': 'K-207' }
            ],
            'subjects': [
                { 'id': 25, 'name': 'Informatika' },
                { 'id': 1, 'name': 'Analýza informačních zdrojů' },
                { 'id': 4, 'name': 'Kybernetická bezpečnost' },
                { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
            ]
        }
    )

    console.log(state)

    useEffect(() => {
        fetch('/gql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            redirect: 'follow', // manual, *follow, error
            body: JSON.stringify({
                "query":
                    `
                query {
                    user(id: ${props.id}) {
                        id
                        name
                        lastname
                        degreeRank
                        email
                        phone
                        areal
                        building
                        room
                        faculty: groupsByType(type: 0) {
                            id
                            name
                        }
                        departments: groupsByType(type: 1) {
                            id
                            name
                        }
                        subjects: groupsByType(type: 2) {
                            id
                            name
                        }
                    }
                }
                `
            }),
        })
            .then(response => response.json())
            .then(data => setState(data.data))
            .then(() => console.log('data logged'))
            .catch(error => console.log('error nacteni'))
    }, [props.id])


    return (
        <TeacherLarge {...props} {...state} />
    )
}
*/

export const TeacherLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
            query {
                user: person(id: ${id}) {
                    id
                    name
                    surname
                    email
                    groups {
                      id
                      name
                      grouptype {
                        id
                        name
                      }
                    }
                    students {
                      person {
                        id
                        name
                        surname
                        email
                      }
                    }
                  }
            }
            `
        }),
    })

export const TeacherLargeStoryBook = (props) => {
    const extendedProps = {
        'id': props.id,
        'name': 'props.name',
        'lastname': 'props.lastname',
        'degreeRank': 'ing. plk.',
        "email": 'props.name.toLowerCase()' + '.' + 'props.lastname.toLowerCase()' + '1@unob.cz',
        'phone': '973 274 160',
        'areal': 'Kasárny Šumavská',
        'building': '5',
        'room': '104',
        'faculty': [
            { 'id': 23, 'name': 'FVT' }
        ],
        'departments': [
            { 'id': 5, 'name': 'K-209' },
            { 'id': 6, 'name': 'K-207' }
        ],
        'subjects': [
            { 'id': 25, 'name': 'Informatika' },
            { 'id': 1, 'name': 'Analýza informačních zdrojů' },
            { 'id': 4, 'name': 'Kybernetická bezpečnost' },
            { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
        ]
    }
    return <TeacherLarge {...extendedProps} {...props} />;
}

export const TeacherLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, TeacherLargeQuery, (response) => response.data.user, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <TeacherLargeStoryBook {...state} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const TeacherPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} />
    )    
}



function RozvrhMedium() {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Rozvrh tento týden</Card.Title>
            </Card.Header>
            <Card.Body>
                <img src={image} alt="Rozvrh" width={'100%'} />
            </Card.Body>
        </Card>
    )
}


function SeznamPredmetu(props) {
    let subjects = props.subjects.map((subject) => (<li><SubjectSmall {...subject} /></li>))
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Předměty</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {subjects}
                </ul>
            </Card.Body>
        </div>
    )
}