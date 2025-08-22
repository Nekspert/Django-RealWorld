import superagentPromise from 'superagent-promise';
import _superagent from 'superagent';

const superagent = superagentPromise(_superagent, global.Promise);

const API_ROOT = 'http://localhost:8000/api';

const encode = encodeURIComponent;
const responseBody = res => {
    const body = res && res.body;

    // Если тело отсутствует — вернуть пустой объект
    if (!body) return {};

    // --- если уже в формате Conduit frontend expects
    // { articles: [...], articlesCount: N }
    if (body.articles !== undefined && body.articlesCount !== undefined) {
        return body;
    }

    // --- если это DRF пагинация: { count, next, previous, results }
    if (body.count !== undefined && body.results !== undefined) {
        const results = body.results;

        // если results — объект { articles: [...], articlesCount: N }
        if (results && results.articles !== undefined && results.articlesCount !== undefined) {
            return {
                articles: results.articles,
                articlesCount: results.articlesCount
            };
        }

        // если results — массив статей
        if (Array.isArray(results)) {
            return {
                articles: results,
                articlesCount: body.count
            };
        }

        // fallback
        return {
            articles: [],
            articlesCount: body.count || 0
        };
    }

    // --- если это стандартный single-entity response: { article: {...} } или { tags: [...] }
    if (body.article !== undefined || body.tags !== undefined || body.user !== undefined || body.profile !== undefined) {
        return body;
    }

    // --- если вернулся просто массив (редко) — преобразуем в ожидемый формат
    if (Array.isArray(body)) {
        return { articles: body, articlesCount: body.length };
    }

    // В остальных случаях отдаем как есть
    return body;
};

let refreshPromise = null;
const tryRequestWithRefresh = fn =>
    fn()
        .then(responseBody)
        .catch(err => {
            const status = err && err.status;
            if (status === 401) {
                if (!refreshPromise) {
                    refreshPromise = superagent
                        .post(`${API_ROOT}/token/refresh/`)
                        .withCredentials()
                        .then(r => {
                            return r;
                        })
                        .catch(e => {
                            throw e;
                        })
                        .finally(() => {
                            refreshPromise = null;
                        });
                }
                return refreshPromise
                    .then(() => {
                        return fn().then(responseBody);
                    })
                    .catch(refreshErr => {
                        throw refreshErr || err;
                    });
            }
            throw err;
        });

const requests = {
    del: url =>
        tryRequestWithRefresh(() => superagent.del(`${API_ROOT}${url}`).withCredentials()),
    get: url =>
        tryRequestWithRefresh(() => superagent.get(`${API_ROOT}${url}`).withCredentials()),
    put: (url, body) =>
        tryRequestWithRefresh(() => superagent.put(`${API_ROOT}${url}`, body).withCredentials()),
    post: (url, body) =>
        tryRequestWithRefresh(() => superagent.post(`${API_ROOT}${url}`, body).withCredentials())
};

const Auth = {
    current: () =>
        requests.get('/user'),
    login: (email, password) =>
        requests.post('/users/login', {user: {email, password}}),
    refresh: (body = {}) =>
        requests.post('/token/refresh/', body),
    register: (username, email, password) =>
        requests.post('/users', {user: {username, email, password}}),
    save: user =>
        requests.put('/user', {user}),
    logout: () =>
        requests.post('/users/logout', {})
};

const Tags = {
    getAll: () => requests.get('/tags')
};

const limit = (count, p) => `limit=${count}&offset=${p ? p * count : 0}`;
const omitSlug = article => Object.assign({}, article, {slug: undefined})
const Articles = {
    all: page =>
        requests.get(`/articles?${limit(10, page)}`),
    byAuthor: (author, page) =>
        requests.get(`/articles?author=${encode(author)}&${limit(5, page)}`),
    byTag: (tag, page) =>
        requests.get(`/articles?tag=${encode(tag)}&${limit(10, page)}`),
    del: slug =>
        requests.del(`/articles/${slug}`),
    favorite: slug =>
        requests.post(`/articles/${slug}/favorite`),
    favoritedBy: (author, page) =>
        requests.get(`/articles?favorited=${encode(author)}&${limit(5, page)}`),
    feed: () =>
        requests.get('/articles/feed?limit=10&offset=0'),
    get: slug =>
        requests.get(`/articles/${slug}`),
    unfavorite: slug =>
        requests.del(`/articles/${slug}/favorite`),
    update: article =>
        requests.put(`/articles/${article.slug}`, {article: omitSlug(article)}),
    create: article =>
        requests.post('/articles', {article})
};

const Comments = {
    create: (slug, comment) =>
        requests.post(`/articles/${slug}/comments`, {comment}),
    delete: (slug, commentId) =>
        requests.del(`/articles/${slug}/comments/${commentId}`),
    forArticle: slug =>
        requests.get(`/articles/${slug}/comments`)
};

const Profile = {
    follow: username =>
        requests.post(`/profiles/${username}/follow`),
    get: username =>
        requests.get(`/profiles/${username}`),
    unfollow: username =>
        requests.del(`/profiles/${username}/follow`)
};

export default {
    Articles,
    Auth,
    Comments,
    Profile,
    Tags,
};
