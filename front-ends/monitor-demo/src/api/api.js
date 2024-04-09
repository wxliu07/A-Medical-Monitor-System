import request from './request'

export default {
    isAdmin(params) {
        return request({
            method: 'GET',
            url: '/database/isAdmin',
            data: params
        })
    },

    isUser(params) {
        return request({
            method: 'GET',
            url: '/database/isUser',
            data: params
        })
    },
}