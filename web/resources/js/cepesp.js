import axios from 'axios';

function getQuery(params) {
    let promise = axios.get('/api/consulta/athena/query', {
        params,
        paramsSerializer: (p) => $.param(p),
    });
    
    return promise.then((response) => {
        return {
            id: response.data.id,
            sql: response.data.sql,
            name: response.data.name,
            table: params.table,
            start: params.start,
            length: params.length
        };
    });
}

function getStatus(query_id) {
    let params = {id: query_id};
    let promise = axios.get('/api/consulta/athena/status', {params});
    
    return promise.then((response) => {
        let {status, message} = response.data;
        return [status, message];
    });
}

function getResult(query_id, start, length) {
    let params = {
        id: query_id,
        start: start,
        length: length,
        format: 'json',
        ignore_version: true
    };
    let promise = axios.get('/api/consulta/athena/result', {params});

    return promise.then((response) => {
        return response.data;
    });
}

function getColumns(params) {
    let promise = axios.get('/api/consulta/athena/columns', {
        params,
        paramsSerializer: (p) => $.param(p),
    });

    return promise.then((response) => {
        return {
            'columns': response.data.columns || [],
            'translated_columns': response.data.translated_columns || {},
            'default_columns': response.data.default_columns || [],
            'descriptions': response.data.descriptions || {},
        }
    });
}

function getYears(job) {
    switch (parseInt(job)) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
            return [2018, 2014, 2010, 2006, 2002, 1998];
        case 11:
        case 12:
        case 13:
            return [2016, 2012, 2008, 2004, 2000];
        default:
            return [];
    }
}

export default {getQuery, getStatus, getResult, getYears, getColumns};