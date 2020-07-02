

fn listen_and_resend_img() {
    let context = zmq::Context::new();
    let publisher = context.socket(zmq::PUB).unwrap();
    publisher.bind("tcp://0.0.0.0:5555").unwrap();

    let context = zmq::Context::new();
    let piper = context.socket(zmq::SUB).unwrap();
    piper.bind("tcp://0.0.0.0:5556").unwrap();
    piper.set_subscribe(b"").expect("Failed set subscription");

    loop {
        let buf = piper.recv_bytes(0).unwrap();
        publisher.send("CAFF", zmq::SNDMORE).unwrap();
        publisher.send(buf, 0).unwrap();
        println!("data sent");
    }
}

fn main() {
    listen_and_resend_img();
}
