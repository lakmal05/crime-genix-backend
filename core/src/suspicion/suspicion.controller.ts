import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Put,
} from '@nestjs/common';
import { SuspicionService } from './suspicion.service';

@Controller('suspicion')
export class SuspicionController {
  constructor(private readonly suspicionService: SuspicionService) {}

  @Post('create')
  create(@Body() data: any) {
    return this.suspicionService.create(data);
  }

  @Get('find-all')
  findAll() {
    return this.suspicionService.findAll();
  }

  @Get('find-by-id' + ':/id')
  findById(@Param('id') id: string) {
    return this.suspicionService.findById(id);
  }

  @Put('update')
  update(@Body() data: any) {
    return this.suspicionService.update(data);
  }

  @Delete('delete/:id')
  delete(@Param('id') id: string) {
    return this.suspicionService.delete(id);
  }
}
