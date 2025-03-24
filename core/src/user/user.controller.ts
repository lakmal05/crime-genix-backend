import { Body, Controller, Param, Post, Query } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('register')
  register(@Body() data: any) {
    return this.userService.register(data);
  }

  @Post('login')
  login(@Body() data: any) {
    return this.userService.login(data.email, data.password);
  }
}
