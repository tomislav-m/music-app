import React from 'react';

interface AlbumProps {
    id: string;
    name: string;
    artist: string;
    imageUrl: string;
}

export default class AlbumSimple extends React.PureComponent<AlbumProps> {
    render() {
        const { imageUrl } = this.props;
        return (
            <React.Fragment>
                <img src={imageUrl} />
            </React.Fragment>
        );
    }
}