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

    getMenu(params) {
        return request({
          url: '/permission/getMenu',
          method: 'post',
          // 这个mock如果是true的话 用的就是线上fastmock的数据
          data: params
        })
    }
}