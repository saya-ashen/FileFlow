import { RefreshTokenResult, UserResult, getLogin, getRegister, refreshTokenApi } from "@/api/user";
import { routerArrays } from "@/layout/types";
import { resetRouter, router } from "@/router";
import { store } from "@/store";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import { removeToken, sessionKey, setToken, type DataInfo } from "@/utils/auth";
import { storageSession } from "@pureadmin/utils";
import { defineStore } from "pinia";
import { userType } from "./types";

export const useUserStore = defineStore({
    id: "pure-user",
    state: (): userType => ({
        // 用户名
        username:
            storageSession().getItem<DataInfo<number>>(sessionKey)?.username ?? "",
        // 页面级别权限
        roles: storageSession().getItem<DataInfo<number>>(sessionKey)?.roles ?? []
    }),
    actions: {
        /** 存储用户名 */
        SET_USERNAME(username: string) {
            this.username = username;
        },
        /** 存储角色 */
        SET_ROLES(roles: Array<string>) {
            this.roles = roles;
        },
        /** 登入 */
        async loginByUsername(data) {
            return new Promise<UserResult>((resolve, reject) => {
                getLogin(data)
                    .then(data => {
                        if (data) {
                            setToken(data.data);
                            resolve(data);
                        }
                    })
                    .catch(error => {
                        reject(error);
                    });
            });
        },
      async registerByUsername(data) {
        return new Promise<UserResult>((resolve, reject) => {
          getRegister(data)
            .then(data => {
              if (data) {
                setToken(data.data);
                resolve(data);
              }
            })
            .catch(error => {
              reject(error);
            });
        });
      },
        /** 前端登出（不调用接口） */
        logOut() {
            this.username = "";
            this.roles = [];
            removeToken();
            useMultiTagsStoreHook().handleTags("equal", [...routerArrays]);
            resetRouter();
            router.push("/login");
        },
        /** 刷新`token` */
        async handRefreshToken(data) {
            return new Promise<RefreshTokenResult>((resolve, reject) => {
                refreshTokenApi(data)
                    .then(data => {
                        if (data) {
                            setToken(data.data);
                            resolve(data);
                        }
                    })
                    .catch(error => {
                        reject(error);
                    });
            });
        }
    }
});

export function useUserStoreHook() {
    return useUserStore(store);
}
