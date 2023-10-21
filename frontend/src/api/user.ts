import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";


export type UserResult = {
  success: boolean;
  data: {
    /** 用户名 */
    username: string;
    /** 当前登陆用户的角色 */
    roles: Array<string>;
    /** `token` */
    access_Token: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refresh_Token: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

export type RefreshTokenResult = {
  success: boolean;
  data: {
    /** `token` */
    access_Token: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refresh_Token: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", baseUrlApi("api/login"), { data, headers: { "Content-Type": "application/x-www-form-urlencoded" } });
  //return http.request<UserResult>("post", "login", { data, headers: { "Content-Type": "application/x-www-form-urlencoded" } });
};

/** 注册 */
export const getRegister = (data?: object) => {
  const reg_data = {
    username: data["username"],
    nickname: data["username"],
    password: data["password"],
    email: "test@test",
  };
return http.request<UserResult>("post", baseUrlApi("api/register"), { data:reg_data, headers: { "Content-Type": "application/json" } });
};

/** 刷新token */
export const refreshTokenApi = (data?: object) => {
  return http.request<RefreshTokenResult>("post", baseUrlApi("api/refreshToken"), { data });
  //return http.request<RefreshTokenResult>("post", "/refreshToken", { data });
};
