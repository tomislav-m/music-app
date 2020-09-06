import React from 'react'
import { AlbumSimple } from '../../Models/Albums';
import { Grid } from 'semantic-ui-react'
import moment from 'moment';

interface AlbumListSimpleState {
    albums: Array<AlbumSimple>
}

export default class AlbumListSimple extends React.PureComponent<{}, AlbumListSimpleState> {

    constructor(props: any) {
        super(props);
        this.state = {
            albums: []
        }
    }

    componentDidMount() {
        const now = moment().format('MM-DD');
        this.getAlbums(now);
    }

    getAlbums = (date: string) => {
        fetch('http://localhost:5000/albums/' + date)
            .then(response => response.json())
            .then((albums: Array<AlbumSimple>) => this.setState({ albums }));
    }

    render() {
        const { albums } = this.state;
        return (
            <Grid columns={4}>
                {
                    albums.map(album =>
                        <Grid.Column key={album.id}>
                            <img src={album.imageUrl} alt={album.name} width="300px" />
                            <h5>{album.artist} - {album.name}</h5>
                        </Grid.Column>
                    )
                }
            </Grid>
        );
    }
}