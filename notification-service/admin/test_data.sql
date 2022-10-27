insert into notify.templates_body (id, title, content, content_type, description, created, modified)
values ('a4625d15-d80d-460a-95f3-7a0716125646', 'Welcome', '<h1>message</h1>', 'html', 'Welcome mailing',
        '2021-06-16 20:14:09.221838 +00:00', '2021-06-16 20:14:09.221838 +00:00');

insert into notify.senders (id, name, email,  created, modified)
values ('370f7912-ed42-4d20-871e-745ee0effcad', 'FirstName LastName', 'email@domain.com',
        '2021-06-16 20:14:09.221838 +00:00', '2021-06-16 20:14:09.221838 +00:00');

insert into notify.templates_notify (id, title, body_id, theme, notification_type, send_from_id,   created, modified)
values ('d52d0e18-0fb2-491f-adf5-22f6f9df0ce1', 'Welcome', 'a4625d15-d80d-460a-95f3-7a0716125646', 'Welcome', 'mail','370f7912-ed42-4d20-871e-745ee0effcad',
        '2021-06-16 20:14:09.221838 +00:00', '2021-06-16 20:14:09.221838 +00:00');


insert into notify.notifications (id, notification_templates_id,  status,
  created, modified)
values ('fdef764b-cb83-42d0-9d9b-300d04b9860e', 'd52d0e18-0fb2-491f-adf5-22f6f9df0ce1', 'new',
        '2021-06-16 20:14:09.221838 +00:00', '2021-06-16 20:14:09.221838 +00:00');

