import {ASYNC_END, ASYNC_START, LOGIN, LOGOUT, REGISTER} from './constants/actionTypes';

const promiseMiddleware = store => next => action => {
    if (isPromise(action.payload)) {
        store.dispatch({type: ASYNC_START, subtype: action.type});

        const currentView = store.getState().viewChangeCounter;
        const skipTracking = action.skipTracking;

        action.payload.then(
            res => {
                const currentState = store.getState();
                if (!skipTracking && currentState.viewChangeCounter !== currentView) {
                    return;
                }
                console.log('RESULT', res);
                // res уже нормализован responseBody (см. agent.js)
                action.payload = res;
                store.dispatch({type: ASYNC_END, promise: action.payload});
                store.dispatch(action);
            },
            error => {
                const currentState = store.getState();
                if (!skipTracking && currentState.viewChangeCounter !== currentView) {
                    return;
                }
                console.log('ERROR', error);

                // Нормализуем тело ошибки в { errors: {...} } — безопасно при разных вариантах err
                let payload;
                // superagent: error.response.body может содержать тело
                if (error && error.response && error.response.body) {
                    const body = error.response.body;
                    if (body.errors) {
                        payload = body; // уже в нужном формате
                    } else if (body.detail) {
                        payload = {errors: {server: [body.detail]}};
                    } else {
                        // body может быть объектом с полями в другом формате -> положим в errors
                        payload = {errors: body};
                    }
                } else if (error && error.response && typeof error.response.text === 'string') {
                    // fallback: сервер вернул текст/HTML
                    payload = {errors: {server: [error.response.text]}};
                } else {
                    // network error or unknown
                    payload = {errors: {server: [error.message || 'Unknown error']}};
                }

                action.error = true;
                action.payload = payload;

                if (!action.skipTracking) {
                    store.dispatch({type: ASYNC_END, promise: action.payload});
                }
                store.dispatch(action);
            }
        );

        return;
    }

    next(action);
};

const localStorageMiddleware = store => next => action => {
    if (action.type === REGISTER || action.type === LOGIN) {
    } else if (action.type === LOGOUT) {
    }
    next(action);
};

function isPromise(v) {
    return v && typeof v.then === 'function';
}


export {promiseMiddleware, localStorageMiddleware}
